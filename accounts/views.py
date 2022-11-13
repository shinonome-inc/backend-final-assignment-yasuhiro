
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.contrib.auth import authenticate


class SignUpView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:home')    
