from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

from .forms import SignUpForm
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.
"""
自定义一个 form的渲染函数 也可以 {{form.as_h}}
"""
def as_h(self):
    return '<h2>hhhhhhhh</h2>'

UserCreationForm.as_h = as_h


def signup(request):
    if request.method == 'POST':
        form  = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save() ## 保存这个form的实例对象 创建user
            auth_login(request,user) ##
            return redirect('home')
    else:
        form  = SignUpForm()   
    return render(request,'signup.html',{'form':form})

class UserUpdateView(UpdateView):
    model = User
    template_name = 'my_account.html'
    success_url = reverse_lazy('home')
    fields = ['username','first_name','last_name','email']

    def get_object(self, queryset=None):

        return self.request.user