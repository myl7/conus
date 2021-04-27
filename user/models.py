from django.db import models
from django.contrib.auth.models import User


class UstcCasCredential(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gid = models.CharField(max_length=60)
