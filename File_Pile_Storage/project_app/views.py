from django.shortcuts import render
from project_app.models import UserInfo

# Create your views here.
def land_index(request):
    return render(request, 'project_app/landing_page.html')

def signin(request):
    return render(request, 'project_app/page-login.html')

def signup(request):
    return render(request, 'project_app/page-register.html')

def files_view(request):
    return render(request, 'project_app/index.html')

def share_view(request):
    return render(request, 'project_app/index1.html')

def profile_settings(request):
    return render(request, 'project_app/app-profile.html')

def about_sec(request):
    return render(request, 'project_app/layout-blank.html')
