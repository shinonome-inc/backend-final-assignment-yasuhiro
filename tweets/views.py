from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView

from tweets.models import Tweet


class HomeView(LoginRequiredMixin, ListView):
    model = Tweet
    context_object_name = "tweets"
    template_name = "tweets/home.html"
    queryset = model.objects.select_related("user").order_by("-created_at")[:10]


class TweetCreateView(LoginRequiredMixin, CreateView):
    model = Tweet
    fields = ["content"]
    template_name = "tweets/create.html"
    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TweetDetailView(LoginRequiredMixin, DetailView):
    model = Tweet
    context_object_name = "tweet"
    template_name = "tweets/detail.html"


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet
    context_object_name = "tweet_delete"
    template_name = "tweets/delete.html"
    success_url = reverse_lazy("tweets:home")

    def test_func(self):
        tweet = self.get_object()
        return self.request.user == tweet.user
