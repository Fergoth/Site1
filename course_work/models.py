from django.db import models
from django.contrib.auth.models import User
from main.models import Profile
# Create your models here.
class Course_Request(models.Model):
    owner_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    topic = models.TextField(max_length=600, blank=True)
    university = models.TextField(max_length=40)
    teacher = models.TextField(max_length=40)
    min_price = models.IntegerField()
    max_price = models.IntegerField()