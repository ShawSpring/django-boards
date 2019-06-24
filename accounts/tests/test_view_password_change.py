from django.test import TestCase
from django.core.urlresolvers import reverse
from django.urls import resolve
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm

# from django.contrib.auth import get_user_model
# User = get_user_model()
from django.contrib.auth.models import User

class PasswordChangeTests(TestCase):
    def setUp(self):
        username = 'john'
        password = 'aaaabbbb'
        email = 'john@163.com'
        user = User.objects.create_user(username=username,password = password,email= email)
        url = reverse('password_change')
        self.client.login(username=username,password = password)
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code,200)
    
    def test_url_resolves_correct_view(self):
        view = resolve('/settings/password/')
        self.assertEqual(view.func.view_class,auth_views.PasswordChangeView)
    
    def test_csrf(self):
        self.assertContains(self.response,'csrfmiddlewaretoken')
    
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form,PasswordChangeForm)
    
    def test_form_inputs(self):
        """
        The view must contians 4 inputs:csrf,old_password,new_password1,new_password2
        """
        self.assertContains(self.response,'<input ',4)
        self.assertContains(self.response,'type="password"',3)


class PasswordChangeRequireLoginTest(TestCase):
    def test_non_login_redirection(self):
        """
        没有登录 应该重定向到登录页面
        """
        
        login_url = reverse('login')
        url = reverse('password_change')
        response = self.client.get(url)
        # self.assertRedirects(response,"%s?next=%s"%(login_url,url))
        self.assertRedirects(response,f"{login_url}?next={url}")


class PasswordChangePostTestCase(TestCase):
    def setUp(self,data={}):
        self.user = User.objects.create_user(username='john',email='john@163.com',password='old_password')
        self.url = reverse('password_change')
        self.client.login(username='john', password='old_password')
        """
        注意： django不会存储原始密码，user.password是hash过的密码，所以下面登录不成功
        # self.client.login(username = self.user.username,password = self.user.password)
        """
        self.response = self.client.post(self.url,data)
        

class PasswordChangeSuccessfulTests(PasswordChangePostTestCase):
    def setUp(self):
        super().setUp({
            'old_password':'old_password',
            'new_password1':'new_password',
            'new_password2':'new_password'
        })

    def test_redirection(self):
        self.assertRedirects(self.response,reverse('password_change_done'))

    def test_password_changed(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))
    
    def test_user_authenticated(self):
        """
        验证user.is_authenticated,但是这个用户不能是self.user,而是页面中拿到的用户
        """
        response = self.client.get(reverse('home'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)
    

class InvalidPasswordChangeTests(PasswordChangePostTestCase):
    def setUp(self):
        super().setUp({
            'old_password':'old_password',
            'new_password1':'new_password',
            'new_password2':'password_new'
        })
    def test_status_code(self):
        """
        an invalid submission should return to the same page
        """
        self.assertEqual(self.response.status_code,200)
        
    def test_form_error(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
    
    def test_didnt_change_password(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('old_password'))
    

    