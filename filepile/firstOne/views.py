from django.shortcuts import render, render_to_response, get_object_or_404
from .models import ValidateUser
from .models import Register
from .models import CloudStorageOperations

# Create your views here.


def index(request):
    if 'user' not in request.session or request.session['user'] == -1:
        request.session['user'] = -1
        return render(request, 'login.html', {})
    return folder(request)


def login(request):
    request.session['user'] = -1
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

    cso = CloudStorageOperations.getInstance(userID=int(request.session['user']))
    fileList = cso.viewFiles()
    return render(request, 'folder.html', {'fileList': fileList, 'user': request.session['user'], 'folderID': cso.currentFolder})


def authenticate(request):
    params = request.POST
    v = ValidateUser()
    check = v.check(params['email'], params['password'])
    tmp1 = {'username': params['email'], 'password': params['password'], 'session_user': -1}

    if check != -1:
        request.session['user'] = check
        cso = CloudStorageOperations.getInstance(int(request.session['user']))
        return folder(request)
    else:
        request.session['user'] = -1
        return render(request, 'login.html', {})


def fileUpload(request):
    params = request.POST
    if 'user' not in request.session or request.session['user'] == -1:
        request.session['user'] = -1
        return render(request, 'login.html', {})

    cso = CloudStorageOperations.getInstance(userID=int(request.session['user']))
    cso.uploadFile(request)
    return folder(request)


def fileDownload(request, slug):
    cso = CloudStorageOperations.getInstance(userID=int(request.session['user']))
    return cso.downloadFile(slug)


def fileDelete(request, slug):
    cso = CloudStorageOperations.getInstance(userID=int(request.session['user']))
    cso.deleteFile(slug)
    return folder(request)