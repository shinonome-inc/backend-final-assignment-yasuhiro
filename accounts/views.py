
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.contrib.auth import authenticate
from django.http import HttpResponse


class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:home')
    
    def signup(request):
        html = "singup.html"
        return HttpResponse(html)
