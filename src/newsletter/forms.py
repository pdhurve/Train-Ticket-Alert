from django import forms
from .models import *
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
	password= forms.CharField(widget=forms.PasswordInput,label="Password")
	password2= forms.CharField(widget=forms.PasswordInput,label="Confirm Password")
	email=forms.EmailField(label="Email Address")

	class Meta:
		model=User
		fields=[
		"username",
		"email",
		"first_name",
		"last_name",
		"password",
		]
	def clean_password2(self):
		password=self.cleaned_data.get("password")
		password2=self.cleaned_data.get("password2")
		if password != password2:
			raise forms.ValidationError("Two Password Must Match.")
		return password

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')

		user = authenticate(username = username, password = password)
		if not user:
			raise forms.ValidationError('ERROR')
			
class TrackForm(forms.ModelForm):
	class Meta:
		model = Track
		fields = [
		"Source_stn_code",
		"destination_stn_code",
		"date_of_journey",
		]

class myDataForm(forms.ModelForm):
	class Meta:
		model = myData
		fields = [
			"Phone",
			"AddressLine",
		]


