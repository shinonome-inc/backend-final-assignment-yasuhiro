from django.contrib.auth import authenticate, get_user_model, login, views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from mysite.settings import LOGIN_REDIRECT_URL

from .forms import LoginForm, SignUpForm

User = get_user_model()


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy(LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return response


class LoginView(views.LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm


class LogoutView(views.LogoutView):
    template_name = "welcome/index.html"


class UserProfileView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.request.POST.get("username")
        return context
