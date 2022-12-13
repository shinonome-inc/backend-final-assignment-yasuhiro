from django.contrib.auth import SESSION_KEY
from django.test import TestCase
from django.urls import reverse

from .models import User


class TestSignUpView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")

    # setUp作業

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_success_post(self):
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, user_data)
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )  # Homeにリダイレクト

        self.assertTrue(
            User.objects.filter(
                username=user_data["username"],
                email=user_data["email"],
            ).exists()
        )  # 追加したDBのレコードと入力データとの一致を確認

        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_form(self):
        empty_data = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }

        response = self.client.post(self.url, data=empty_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)

        form = response.context["form"]
        self.assertEqual(form.errors["username"][0], "このフィールドは必須です。")
        self.assertEqual(form.errors["email"][0], "このフィールドは必須です。")
        self.assertEqual(form.errors["password1"][0], "このフィールドは必須です。")
        self.assertEqual(form.errors["password2"][0], "このフィールドは必須です。")

    def test_failure_post_with_empty_username(self):
        username_empty_data = {
            "username": "",
            "email": "qq123456@example.com",
            "password1": "qq123456qq",
            "password2": "qq123456qq",
        }

        response = self.client.post(self.url, data=username_empty_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)

        form = response.context["form"]
        self.assertEqual(form.errors["username"][0], "このフィールドは必須です。")

    def test_failure_post_with_empty_email(self):
        email_empty_data = {
            "username": "Qq123456",
            "email": "",
            "password1": "qq123456qq",
            "password2": "qq123456qq",
        }

        response = self.client.post(self.url, data=email_empty_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)

        form = response.context["form"]
        self.assertEqual(form.errors["email"][0], "このフィールドは必須です。")

    def test_failure_post_with_empty_password(self):
        password_empty_data = {
            "username": "Qq123456",
            "email": "qq123456@example.com",
            "password1": "",
            "password2": "",
        }

        response = self.client.post(self.url, data=password_empty_data)
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password1"][0], "このフィールドは必須です。")
        self.assertEqual(form.errors["password2"][0], "このフィールドは必須です。")
        self.assertEqual(User.objects.all().count(), 0)

    def test_failure_post_with_duplicated_user(self):
        duplicated_user_data = {
            "username": "Qq123456",
            "email": "qq123456@example.com",
            "password1": "qq123456qq",
            "password2": "qq123456qq",
        }

        User.objects.create_user(
            username="Qq123456",
            email="qq123456@example.com",
            password="qq123456qq",
        )

        response = self.client.post(self.url, data=duplicated_user_data)
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertEqual(form.errors["username"], ["同じユーザー名が既に登録済みです。"])
        self.assertEqual(form.errors["email"], ["この Email address を持った ユーザー が既に存在します。"])
        self.assertEqual(User.objects.all().count(), 1)

    def test_failure_post_with_invalid_email(self):
        invalid_email_data = {
            "username": "Qq123456",
            "email": "qq123456",
            "password1": "qq123456qq",
            "password2": "qq123456qq",
        }

        response = self.client.post(self.url, data=invalid_email_data)
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertEqual(form.errors["email"], ["有効なメールアドレスを入力してください。"])
        self.assertEqual(User.objects.all().count(), 0)

    def test_failure_post_with_too_short_password(self):
        short_password_data = {
            "username": "qwer46813",
            "email": "diqwh3012@example.com",
            "password1": "qq12345",
            "password2": "qq12345",
        }

        response = self.client.post(self.url, data=short_password_data)
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertEqual(form.errors["password2"], ["このパスワードは短すぎます。最低 8 文字以上必要です。"])
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_password_similar_to_username(self):
        password_similar_to_username_data = {
            "username": "qq123456qq",
            "email": "qq123456@example.com",
            "password1": "qq123456qq",
            "password2": "qq123456qq",
        }

        response = self.client.post(self.url, data=password_similar_to_username_data)
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertEqual(form.errors["password2"], ["このパスワードは ユーザー名 と似すぎています。"])
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_only_numbers_password(self):
        only_number_password_data = {
            "username": "Qq123456",
            "email": "jdowao312@example.com",
            "password1": "1357924680",
            "password2": "1357924680",
        }

        response = self.client.post(self.url, data=only_number_password_data)
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertEqual(form.errors["password2"][0], "このパスワードは一般的すぎます。")
        self.assertEqual(form.errors["password2"][1], "このパスワードは数字しか使われていません。")
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_mismatch_password(self):
        mismatch_password_data = {
            "username": "Qq123456",
            "email": "qq123456@example.com",
            "password1": "qq123456qq",
            "password2": "qq123456",
        }

        response = self.client.post(self.url, data=mismatch_password_data)
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertEqual(form.errors["password2"], ["確認用パスワードが一致しません。"])
        self.assertEqual(User.objects.all().count(), 0)

"""
class TestLoginView(TestCase):
    def setUp(self):
        pass

    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_empty_password(self):
        pass


class TestLogoutView(TestCase):
    def setUp(self):
        pass

    def test_success_get(self):
        pass


class TestUserProfileView(TestCase):
    def test_success_get(self):
        pass


class TestUserProfileEditView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_user(self):
        pass

    def test_failure_post_with_self(self):
        pass


class TestUnfollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowingListView(TestCase):
    def test_success_get(self):
        pass


class TestFollowerListView(TestCase):
    def test_success_get(self):
        pass
"""
 
