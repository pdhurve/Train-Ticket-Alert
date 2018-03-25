# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .forms import RegistrationForm
from .models import *
# Register your models here.

# class SignUpAdmin(admin.ModelAdmin):
# 	"""docstring for SignUpAdmin"""
# 	list_display = ["__str__", 'timestamp', 'updated']
# 	form = SignUp
# 	'''
# 	class Meta:
# 		model = SignUp
# 	'''

# class myDataAdmin(admin.ModelAdmin):
# 	"""docstring for SignUpAdmin"""
# 	list_display = ["__str__", 'timestamp', 'updated']
# 	form = myData
# 	class Meta:
# 		model = myData

# class TrackAdmin(admin.ModelAdmin):
#  	"""docstring for SignUpAdmin"""
#  	list_display = ["__str__", 'timestamp', 'updated']
#  	form = Track
#  	class Meta:
#  		model = Track

# admin.site.register(myData, myDataAdmin)
# admin.site.register(Track, TrackAdmin)

admin.site.register(myData)
admin.site.register(Track)




