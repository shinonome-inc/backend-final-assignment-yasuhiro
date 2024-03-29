from django.conf import settings
from django.db import models


class Tweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def liked_count(self):
        return self.likes.count()

    def __str__(self):
        return self.content


class Like(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["tweet", "user"], name="unique_like")]
