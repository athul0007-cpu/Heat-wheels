from django.contrib.auth.models import User
from django.db import models


class SupportMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=140)
    message = models.TextField()
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Support request: {self.subject}"


class FAQ(models.Model):
    question = models.CharField(max_length=180)
    answer = models.TextField()
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.question
