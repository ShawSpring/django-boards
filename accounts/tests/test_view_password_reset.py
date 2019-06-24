from django.test import TestCase
from django.contrib.auth import  views as auth_views
from django.contrib.auth.forms import PasswordResetForm
# from django.contrib.auth.models import User
from boards.models import User
from django.core.urlresolvers import reverse
from django.urls import resolve
from django.core import  mail

class PasswordResetTests(TestCase):

    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)
    
    def test_status_code(self):
        self.assertEqual(self.response.status_code,200)
    
    def test_password_reset_view_function(self):
        view = resolve('/reset/')
        self.assertEqual(view.func.view_class,auth_views.PasswordResetView)

    def test_csrf(self):
        self.assertContains(self.response,'csrfmiddlewaretoken')
    
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form,PasswordResetForm)
    
    def test_form_inputs(self):
        self.assertContains(self.response,'<input ',2)
        self.assertContains(self.response,'type="email"',1)

class SuccessfulPassswordResetTests(TestCase):
    def setUp(self):
        email = 'chunlaixiao@163.com'
        User.objects.create_user(username='chunlaixiao',password='aaaabbbb',email=email)
        url = reverse('password_reset')
        self.response  =  self.client.post(url,{'email':email})
    
    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response,url)  

    def test_send_password_reset_email(self):
        self.assertEqual(1,len(mail.outbox))  


class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(url,{'email':'dontexistemail@email.com'})

    def test_redirection(self):
        
        """
        即使是 数据库中非法的email，也应该重定向
        """
        url = reverse('password_reset_done')
        self.assertRedirects(self.response,url)

    def test_no_reset_email_sent(self):
        self.assertEqual(0,len(mail.outbox))
        
class PasswordResetDoneTest(TestCase):
    def setUp(self):
        url=reverse('password_reset_done')
        self.response = self.client.get(url)
    
    def test_status_code(self):
        self.assertEqual(self.response.status_code,200)
    
    def test_view_function(self):
        view = resolve('/reset/done/')
        self.assertEqual(view.func.view_class,auth_views.PasswordResetDoneView)


class PasswordResetComplete(TestCase):
    def setUp(self):
        url = reverse('password_reset_complete')
        self.response = self.client.get(url)
    
    def test_status_code(self):
        self.assertEqual(self.response.status_code,200)

    def test_view_function(self):
        view = resolve('/reset/complete/')
        self.assertEqual(view.func.view_class,auth_views.PasswordResetCompleteView)