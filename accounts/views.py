from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import LoginForm, SignUpForm

User = get_user_model()


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

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


class LoginView(views.LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm


class LogoutView(views.LogoutView):
    pass


class UserProfileView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = get_object_or_404(
            User, username=self.kwargs.get("username")
        )

        return context
