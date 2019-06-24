from django.test import TestCase
from django.core.urlresolvers import resolve
from django.urls import reverse

from ..forms import SignUpForm
# Create your tests here.
from boards import models

from ..views import signup

class SignupTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response= self.client.get(url)

    def test_signup_status_code(self):
        self.assertEqual(self.response.status_code,200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEqual(view.func,signup)
    
    def test_csrf(self):
        self.assertContains(self.response,"csrfmiddlewaretoken")
    
    def test_contains_form(self):
        form  = self.response.context.get('form')
        self.assertIsInstance(form,SignUpForm)

    def test_form_input(self):
        """
        这个视图应该有5个 input, csrf username email password1 password2
        不能多，不能 后续增加 form字段
        """
        self.assertContains(self.response,'<input',5)
        self.assertContains(self.response,'type="text"',1)
        self.assertContains(self.response,'type="email"',1)
        self.assertContains(self.response,'type="password"',2)

class SuccessfulSignupTest(TestCase):
    def setUp(self):
        self.url = reverse('signup')
        data={
            'username':'john',
            'email':'chunlaixiao@163.com',
            'password1':'aaaabbbb',
            'password2':'aaaabbbb'
        }
        self.response = self.client.post(self.url,data)
        self.home_url = reverse('home')

    def	test_redirection(self):
	    self.assertRedirects(self.response,	self.home_url)

    def test_user_creation(self):
        self.assertTrue(models.User.objects.exists())

    def test_user_authentication(self):
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

class InvalidSignupTests(TestCase):
    def setUp(self):
        self.url = reverse('signup')
        data={
            'username':'john',
            'password1':'aaaabbbb',
            'password2':'xxxxxxxx'
        }
        self.response = self.client.post(self.url,data =data)
        self.home_url = reverse('home')
    
    def test_signup_status_code(self):
        self.assertEqual(self.response.status_code,200)
    
    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(models.User.objects.exists())