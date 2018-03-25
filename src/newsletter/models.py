# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class myData(models.Model):
	User=models.ForeignKey(User)
	Phone=models.DecimalField(max_digits=10, decimal_places=False,blank=False)
	AddressLine=models.CharField(max_length=500,blank=True,null=True)
	Updated_at=models.DateTimeField(auto_now_add=False,auto_now=True)
	Created_at=models.DateTimeField(auto_now_add=True,auto_now=False)
	def __str__(self):
		return str(self.User.username)


class Track(models.Model):
	user = models.ForeignKey(User)
	Source_stn_code = models.CharField(max_length=500,blank=True,null=True)
	destination_stn_code = models.CharField(max_length=500,blank=True,null=True)
	date_of_journey =models.DateField(blank = True, null = True)
	def __str__(self):
		return str(self.user.username)

