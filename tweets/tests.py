from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Tweet

User = get_user_model()


class TestHomeView(TestCase):
    def setUp(self):
        self.url = reverse("tweets:home")
        self.user = User.objects.create_user(
            username="testuser01",
            email="testuser01@example.com",
            password="password15432",
        )
        self.client.login(username="testuser01", password="password15432")
        Tweet.objects.create(user=self.user, content="テスト投稿01")
        Tweet.objects.create(user=self.user, content="テスト投稿02")

    def test_success_get(self):
        response = self.client.get(reverse("tweets:home"))
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(response.context["tweets"], Tweet.objects.all(), ordered=False)


class TestTweetCreateView(TestCase):
    def setUp(self):
        self.url = reverse("tweets:create")
        self.user = User.objects.create_user(
            username="testuser01",
            email="testuser01@example.com",
            password="password15432",
        )
        self.client.login(username="testuser01", password="password15432")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/create.html")

    def test_success_post(self):
        data = {"content": "テスト投稿01"}
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse("tweets:home"), status_code=302, target_status_code=200)

    def test_failure_post_with_empty_content(self):
        data = {"content": ""}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertEqual(form.errors["content"], ["このフィールドは必須です。"])
        self.assertFalse(Tweet.objects.exists())

    def test_failure_post_with_too_long_content(self):
        data = {"content": "a" * 151}
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, 200)
        form = response.context["form"]
        self.assertEqual(form.errors["content"], ["この値は 150 文字以下でなければなりません( 151 文字になっています)。"])
        self.assertFalse(Tweet.objects.exists())


class TestTweetDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser01",
            email="testuser01@example.com",
            password="password15432",
        )
        self.test_tweet = Tweet.objects.create(user=self.user, content="テスト投稿01")
        self.client.login(username="testuser01", password="password15432")

    def test_success_get(self):
        response = self.client.get(reverse("tweets:detail", kwargs={"pk": self.test_tweet.pk}))
        self.assertEqual(response.status_code, 200)
        context = response.context
        self.assertEqual(context["tweet"], self.test_tweet)


class TestTweetDeleteView(TestCase):
    def setUp(self):
        self.user01 = User.objects.create_user(
            username="testuser01",
            email="testuser01@example.com",
            password="password15432"
        )
        self.user02 = User.objects.create_user(
            username="testuser02",
            email="testuser02@example.com",
            password="password130974"
        )
        self.tweet01 = Tweet.objects.create(user=self.user01, content="テスト投稿01")
        self.tweet02 = Tweet.objects.create(user=self.user02, content="テスト投稿02")
        self.client.login(username="testuser01", password="password15432")

    def test_success_post(self):
        response = self.client.post(reverse("tweets:delete", kwargs={"pk": self.tweet01.pk}))
        self.assertRedirects(response, reverse("tweets:home"), status_code=302)
        self.assertFalse(Tweet.objects.filter(content="testtweet1").exists())

    def test_failure_post_with_not_exist_tweet(self):
        response = self.client.post(reverse("tweets:delete", kwargs={"pk": 1000}))
        self.assertEquals(response.status_code, 404)
        self.assertEquals(Tweet.objects.count(), 2)

    def test_failure_post_with_incorrect_user(self):
        response = self.client.post(reverse("tweets:delete", kwargs={"pk": self.tweet02.pk}))
        self.assertEqual(response.status_code, 403)
        self.assertEquals(Tweet.objects.count(), 2)


"""
class TestFavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_favorited_tweet(self):
        pass


class TestUnfavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_unfavorited_tweet(self):
        pass
"""
