from django.db import models
from django.contrib.auth.models import User


class Notice(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notices')
    to_users = models.ManyToManyField(User, related_name='received_notices')
    title = models.CharField(max_length=60, blank=True)
    body = models.CharField(max_length=510)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} | Created at {self.create_date}'
