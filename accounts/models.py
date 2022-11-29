from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(verbose_name="email address")


# class FriendShip(models.Model):
#     pass
