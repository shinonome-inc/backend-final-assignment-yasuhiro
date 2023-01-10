from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import LoginForm, SignUpForm

User = get_user_model()


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return response
        else:
            return redirect("welcome:top")


class LoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm


class LogoutView(LoginRequiredMixin, LogoutView):
    pass


class UserProfileView(LoginRequiredMixin, DetailView):
    def get(self, request, *args, **kwargs):
        requested_user = get_object_or_404(User, username=kwargs.get("username"))
        requested_username = requested_user.get_username()
        context = {
            "requested_username": requested_username,
        }
        return render(request, "accounts/profile.html", context)
