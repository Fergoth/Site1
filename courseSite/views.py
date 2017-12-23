from django.http import *
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from main.forms import SignUpForm
from django.contrib.auth.models import Permission
from main.models import Wallet, Profile

def login_user(request):
    logout(request)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
        elif username and password:
            return render(request,'login.html', {
                'error': 'Ошибка авторизации',
            })
        else:
            return render(request,'login.html')
    else:
        return render(request,'login.html')


def main_page(request):
    return HttpResponse('Это главная страница!')


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            add_perm(user, form.cleaned_data.get('perm'))
            w = Wallet.objects.create(balanse=0)
            Profile.objects.create(user=user, wallet=w)
            user.profile.save()
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

    
def add_perm(user, perm):
    permission = Permission.objects.get(codename=perm)
    user.user_permissions.add(permission)