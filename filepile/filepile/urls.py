"""filepile URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from firstOne import views as view
from django.urls import include, re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view.index),
    path('login/', view.login),
    path('logout/', view.logout),
    path('folder/', view.folder),
    path('signup/', view.signup),
    path('register/', view.register),
    path('authenticate/', view.authenticate),
    path('file_upload/', view.fileUpload),
    re_path(r'^file_download/(.*)$',view.fileDownload),
    re_path(r'^file_delete/(.*)$',view.fileDelete),

]
