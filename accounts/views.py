from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, View

from accounts.models import FriendShip, User
from tweets.models import Like, Tweet

from .forms import LoginForm, SignUpForm


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


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = "profile_user"
    template_name = "accounts/profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tweets"] = Tweet.objects.select_related("user").filter(user=self.object).order_by("-created_at").all()
        context["is_following"] = FriendShip.objects.filter(following=self.request.user, follower=self.object).exists()
        context["following_numbers"] = FriendShip.objects.filter(following=self.object).count()
        context["followers_numbers"] = FriendShip.objects.filter(follower=self.object).count()
        context["liked_tweets"] = (
            Like.objects.select_related("user").filter(user=self.request.user).values_list("tweet", flat=True)
        )
        return context


class FollowingListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = "folloing_list"
    template_name = "accounts/following_list.html"

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs["username"])
        return self.user.followers.all().order_by("-date_joined")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["target_user"] = self.user
        return context


class FollowerListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = "follower_list"
    template_name = "accounts/follower_list.html"

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs["username"])
        return self.user.followings.all().order_by("-date_joined")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["target_user"] = self.user
        return context


class FollowView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs["username"])

        if user == self.request.user:
            messages.add_message(self.request, messages.ERROR, "自分自身をフォローすることはできません")
            return redirect("tweets:home")

        if self.request.user.followers.filter(username=user.username).exists():
            messages.add_message(self.request, messages.WARNING, "すでにフォローしています。")
            return redirect("tweets:home")

        self.request.user.followers.add(user)
        messages.add_message(self.request, messages.SUCCESS, "フォローしました。")
        return redirect("tweets:home")


class UnFollowView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs["username"])

        if user == self.request.user:
            messages.add_message(self.request, messages.ERROR, "自分自身をフォロー解除することはできません。")
            return redirect("tweets:home")

        if not self.request.user.followers.filter(username=user.username).exists():
            messages.add_message(self.request, messages.ERROR, "フォローしていません。")
            return redirect("tweets:home")

        self.request.user.followers.remove(user)
        messages.add_message(self.request, messages.SUCCESS, "フォローを解除しました。")
        return redirect("tweets:home")
