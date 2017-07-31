from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models

from group.models import group
from utils.fields import CustomImageField


# User
#   pk
# 	email(id)		EmailField					unique=true
# 	password
# 	nickname		CharField					unique=true, max_length=20
# 	profile_img		CustomImageField			upload_to=user, blank=true
# 	gender			CharField					max_length=1, choices=F/M, null=true
# 	birth_year		IntegerField
# 	birth_month		IntegerField
# 	birth_day		IntegerField
# 	hobby			CharField
# 	region			CharField
# 	group			ManyToManyField(Group)

class User(AbstractUser):
    USER_GENDER_FEMALE = 'f'
    USER_GENDER_MALE = 'm'
    USER_GENDER_CHOICE = (
        (USER_GENDER_FEMALE, 'Female'),
        (USER_GENDER_MALE, 'Male'),
    )

    username = models.EmailField(unique=True)
    nickname = models.CharField(max_length=24)
    profile_img = CustomImageField(
        upload_to='user/%Y/%m/%d/',
        blank=True,
        default_static_image='images/profile.png',
    )
    gender = models.CharField(max_length=1, choices=USER_GENDER_CHOICE)
    birth_year = models.IntegerField(validators=[MaxValueValidator(9999)])
    birth_month = models.IntegerField(validators=[MaxValueValidator(12)])
    birth_day = models.IntegerField(validators=[MaxValueValidator(31)])
    hobby = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    joined_group = models.ManyToManyField('group.Group')

    def __str__(self):
        return self.nickname or self.email