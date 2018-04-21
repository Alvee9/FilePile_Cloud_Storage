from django.shortcuts import render, render_to_response, get_object_or_404
from .models import ValidateUser
from .models import Register
# Create your views here.


def index(request):
    return render(request, 'index.html', {})


def login(request):
    return render(request, 'login.html', {})


def logout(request):
    request.session['user'] = -1
    return render(request, 'login.html', {})


def signup(request):
    request.session['user'] = -1
    return render(request, 'signup.html', {})


def register(request):
    params = request.POST
    r = Register()
    r.register(params['email'], params['name'], params['password'])
    return render(request, 'login.html', {})


def folder(request):
    if 'user' not in request.session or request.session['user'] == -1:
        request.session['user'] = -1
        return render(request, 'login.html', {})
    return render(request, 'folder.html', {})


def upload(request):
    return render(request, 'folder.html', {})


def authenticate(request):
    params = request.POST
    v = ValidateUser()
    check = v.check(params['email'], params['password'])
    tmp1 = {'username': params['email'], 'password': params['password'], 'session_user': -1}

    if check != -1:
        request.session['user'] = check
        tmp1['session_user'] = check
        return render(request, 'index.html', {'tmp1': tmp1})
    else:
        request.session['user'] = -1
        return render(request, 'login.html', {'tmp1': tmp1})