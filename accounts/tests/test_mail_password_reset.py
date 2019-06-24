from django.test import TestCase
from django.core import mail
from boards.models import User
from django.urls import reverse

class PasswordResetEmailTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='john',email='john@163.com',password='123')
        url = reverse('password_reset')
        self.response = self.client.post(url,{'email':"john@163.com"})
        self.email = mail.outbox[0]
    
    def test_email_subject(self):
        self.assertEqual("[Django Boards] please reset your password",self.email.subject)
    
    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm',kwargs={
            'uidb64':uid,
            'token':token
        })
        self.assertIn(password_reset_token_url,self.email.body)
        self.assertIn("john@163.com",self.email.body)
        self.assertIn("john",self.email.body)

    def test_email_to(self):
        self.assertEqual(["john@163.com",],self.email.to)

        
        