from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin

from unimoregym.models import Corso

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from .forms import SignUpClientForm, SignUpOwnerForm
from django.contrib.auth.mixins import PermissionRequiredMixin

def homepage(request):
    return render(request, template_name="home.html")

class GymUserLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('unimoregym:homeGym')


class GymUserLogoutView(LogoutView):
    template_name = 'registration/logged_out.html'

class SignUpOwnerView(PermissionRequiredMixin, CreateView):
    permission_required = "is_staff"
    form_class = SignUpOwnerForm
    template_name = 'registration/sign_up.html'
    success_url = reverse_lazy('login')


class SignUpView(CreateView):
    form_class = SignUpClientForm
    template_name = 'registration/sign_up.html'
    success_url = reverse_lazy("login")
