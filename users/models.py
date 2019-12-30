# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    secret_otp = models.CharField(max_length=600, null=True, blank=True)
    secret_hash = models.CharField(max_length=600, null=True, blank=True)
    avatar = models.CharField(max_length=800, null=True, default="assets/images/demo/users/face11.jpg")
    company = models.CharField(max_length=800,null=True,default="GeneTherapy")
    mobile = models.CharField(max_length=20,null=True,default='N/A')
    domain = models.CharField(max_length=2000,null=True,default=None)
    


    class Meta:
        db_table = "users"
        verbose_name_plural = "Users"
        verbose_name = "User"

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "username": self.username

        }

    def get_user_full_name(self):
        return "{0} {1}".format(self.first_name,self.last_name)

    def get_user_details(self):
        return {
            "full_name" : "{0} {1}".format(self.first_name,self.last_name),
            "user_id" : self.id,
            "username" : self.username
        }
