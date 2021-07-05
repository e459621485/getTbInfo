from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    nid = models.AutoField(primary_key=True)

    def __str__(self):
        return self.username

# Create your models here.
