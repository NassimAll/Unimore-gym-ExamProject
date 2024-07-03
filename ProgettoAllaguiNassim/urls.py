"""
URL configuration for ProgettoAllaguiNassim project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

from .gestione_functions import start_thread
from .views import *
from .initDatabase import *


urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^$|^\/$|^home\/$", homepage, name="home"),
    path("unimoregym/", include("unimoregym.urls")),
    path('register/client/', SignUpView.as_view(), name='register_client'),
    path('register/owner/', SignUpOwnerView.as_view(), name='register_owner'),
    path('login/', GymUserLoginView.as_view(), name='login'),
    path('logout/', GymUserLogoutView.as_view(), name='logout'),
    path('gymapi/', include("gmyapi.urls"))
]

#per inizializzare la media directory
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#Inizializzatoo una volta sola
#erase_db()
#init_db()
#start_thread() #thread per la rimozione dei valori sccaduti nel db


