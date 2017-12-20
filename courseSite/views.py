from django.http import *
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

def login_user(request):
    logout(request)
    username = password = ''
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
