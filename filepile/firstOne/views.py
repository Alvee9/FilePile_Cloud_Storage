from django.shortcuts import render, render_to_response, get_object_or_404

# Create your views here.


def index(request):
    return render(request, 'index.html', {})


def login(request):
    return render(request, 'login.html', {})


def logout(request):
    return render(request, 'index.html', {})


def folder(request):
    return render(request, 'folder.html', {})


def upload(request):
    return render(request, 'folder.html', {})
