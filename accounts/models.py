from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField("email address", unique=True)

    followings = models.ManyToManyField(
        "self",
        related_name="followers",
        through="FriendShip",
        through_fields=("follower", "following"),
        symmetrical=False,
    )


class FriendShip(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="follower_friendships", on_delete=models.CASCADE
    )
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="following_users", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["follower", "following"], name="unique_friendship")]
