from django.db import models
from django.contrib.auth.models import User
from main.models import Profile


class Course_Request(models.Model):
    owner_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    topic = models.TextField(max_length=60)
    description = models.TextField(max_length=600,default='')
    university = models.TextField(max_length=40,blank=True)
    teacher = models.TextField(max_length=40,blank=True)
    min_price = models.IntegerField(default=10)
    max_price = models.IntegerField(default=100)
    on_processing = models.BooleanField(default=False)
    

class Request_offers(models.Model):
    course_request = models.ForeignKey(Course_Request, on_delete=models.CASCADE)
    owner_performer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    price = models.IntegerField(default=1000)
    
    class Meta:
        unique_together = (("course_request", "owner_performer"),)
