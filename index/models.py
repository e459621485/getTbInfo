from django.db import models


class tbInfo(models.Model):
    title = models.CharField(max_length=300)
    price = models.CharField(max_length=20)
    seller = models.CharField(max_length=300)
    img = models.CharField(max_length=300)
    datetime = models.DateTimeField(auto_now=True)

# Create your models here.
