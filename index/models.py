from django.db import models
from django.contrib.auth.models import User


class tbInfo(models.Model):
    title = models.CharField(max_length=300)
    price = models.CharField(max_length=20)
    seller = models.CharField(max_length=300)
    img = models.CharField(max_length=300)
    url = models.CharField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)

# Create your models here.
