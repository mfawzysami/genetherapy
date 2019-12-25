# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from users.models import User

class Component(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField(null=True,blank=True)
    user = models.ForeignKey(User)

    class Meta:
        db_table = "components"
        verbose_name = "Component"
        verbose_name_plural = "Components"

