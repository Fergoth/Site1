from django.db import models
from django.contrib.auth.models import User
from main.models import Profile
from django.forms.models import modelform_factory

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
    price = models.IntegerField(default=0)
    
    class Meta:
        unique_together = (("course_request", "owner_performer"),)

class Approved_course(models.Model):
    owner_user = models.ForeignKey(Profile,related_name='owner_user',on_delete=models.CASCADE,null=True)
    owner_performer = models.ForeignKey(Profile,related_name='owner_performer',on_delete=models.SET_NULL,null=True)
    price = models.IntegerField(default=0)
    topic = models.TextField(max_length=60)
    description = models.TextField(max_length=600, default='')
    university = models.TextField(max_length=40, blank=True)
    ready = models.BooleanField(default=False)
    file = models.FileField(upload_to='uploads/',blank=True)
    
class Transactions(models.Model):
    from_profile = models.ForeignKey(Profile,related_name='from_profile',on_delete=models.SET_NULL,null=True)
    to_profile = models.ForeignKey(Profile,related_name='to_profile', on_delete=models.SET_NULL,null=True)
    sum = models.IntegerField(default=0)
    