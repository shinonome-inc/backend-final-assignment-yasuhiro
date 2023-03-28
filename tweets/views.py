from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, View

from tweets.models import Like, Tweet


class HomeView(LoginRequiredMixin, ListView):
    model = Tweet
    context_object_name = "tweets"
    template_name = "tweets/home.html"
    ordering = "-created_at"
    queryset = Tweet.objects.prefetch_related("likes").select_related("user").all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["liked_tweets"] = Like.objects.filter(user=self.request.user).values_list("tweet", flat=True)
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["liked_tweets"] = Like.objects.filter(user=self.request.user).values_list("tweet", flat=True)
        return context


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet
    context_object_name = "tweet_delete"
    template_name = "tweets/delete.html"
    success_url = reverse_lazy("tweets:home")

    def test_func(self):
        tweet = self.get_object()
        return self.request.user == tweet.user


class LikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=kwargs["pk"])
        Like.objects.get_or_create(user=self.request.user, tweet=tweet)
        context = {
            "liked_count": tweet.likes.count(),
            "tweet_id": tweet.id,
            "is_liked": True,
        }
        return JsonResponse(context)


class UnlikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=kwargs["pk"])
        Like.objects.filter(user=self.request.user, tweet=tweet).delete()
        context = {
            "liked_count": tweet.likes.count(),
            "tweet_id": tweet.id,
            "is_liked": False,
        }
        return JsonResponse(context)
