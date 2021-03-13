from django.contrib.auth.models import AbstractUser
from django.db import models


class ShopUser(AbstractUser):
    email = models.EmailField('email', unique=True)
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveSmallIntegerField(verbose_name='возраст')

# Create your models here.
