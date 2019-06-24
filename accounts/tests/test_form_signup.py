from django.test import TestCase
from ..forms import  SignUpForm

class SignUpFormTests(TestCase):
    def setUp(self):
        pass
    
    def test_form_has_fields(self):
        form = SignUpForm()
        excepted = ['username','email','password1','password2']
        actual = list(form.fields)
        self.assertSequenceEqual(excepted,actual)