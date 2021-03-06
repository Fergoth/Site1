from django.http import *
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from main.forms import SignUpForm
from django.contrib.auth.models import Permission
from main.models import Wallet, Profile

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/course')
        elif username and password:
            return render(request,'main.html', {
                'error': 'Ошибка авторизации',
            })
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def main_page(request):
    logout(request)
    return render(request, 'main.html')


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            add_perm(user, form.cleaned_data.get('perm'))
            p = Profile.objects.create(user=user)
            Wallet.objects.create(profile=p, balance=0)
            user.profile.save()
            login(request, user)
            return HttpResponseRedirect('/course')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

    
def add_perm(user, perm):
    permission = Permission.objects.get(codename=perm)
    user.user_permissions.add(permission)
