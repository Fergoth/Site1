from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    biography = models.TextField(max_length=600, blank=True)
    location = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    rate = models.IntegerField(default=0)
    
    class Meta:
        permissions = (("customer", "Базовый пользователь"),
                       ("performer", "Исполнитель"),
                       ("reviewer", "Рецензент"),)
        
        
class Wallet(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True,default=0)
    balance = models.IntegerField(default=0)

 





