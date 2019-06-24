from django.test import TestCase

from django import forms

from ..templatetags.form_tags import field_type,input_class


class ExampleForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput())
    class meta:
        fields = ('name','password')

class FiledTypeTests(TestCase):
    def setUp(self):
        pass
    def test_field_widget_type(self):
        form = ExampleForm()
        self.assertEqual('TextInput',field_type(form['name']))
        self.assertEqual('PasswordInput',field_type(form['password']))

    
class InputClassTests(TestCase):
    def test_unbound_filed_initial_state(self):
        form = ExampleForm()
        self.assertEqual('form-control',str.strip(input_class(form['name'])))

    def test_valid_bound_field(self):
        form = ExampleForm({
            'name':'john',
            'password':'aaaabbbb'
        })
        self.assertEqual('form-control is-valid',input_class(form['name']))
        self.assertEqual('form-control ',input_class(form['password']))
    
    def test_invalid_bound_field(self):
        form = ExampleForm({
            'name':'',
            'password':'123'
        })
        self.assertEqual('form-control is-invalid',input_class(form['name']))
        self.assertEqual('form-control ',input_class(form['password']))