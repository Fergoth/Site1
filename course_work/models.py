from django.db import models
from django.contrib.auth.models import User
from main.models import Profile


class Course_Request(models.Model):
    owner_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    topic = models.TextField(max_length=600)
    university = models.TextField(max_length=40,blank=True)
    teacher = models.TextField(max_length=40,blank=True)
    min_price = models.IntegerField(default=10)
    max_price = models.IntegerField(default=100)

