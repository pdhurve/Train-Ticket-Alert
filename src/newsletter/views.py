# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)
import json
import datetime
import urllib
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
#from django.core.exceptions import ValidationError
from django.forms import ValidationError
API_KEY="5ofvff6ety"
# Create your views here.
def home(request):
	return render(request, "homepage.html", {})

def signup(request):
	title = "Sign Up Form %s" %(request.user)
	form  = RegistrationForm(request.POST or None)
	
	context = {
		"template_title" : title,
		"form" : form
	}

	if form.is_valid():
		user=form.save(commit=False)
		username=form.cleaned_data.get('username')
		password=form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		new_user = authenticate(username = username, password = password)
		auth_login(request, new_user)
		if not user:
			raise ValidationError('User Not Found')
		context = {
			"title" : "Thank You"
		}
	if request.user.is_authenticated():
		return render(request, "homepage.html", context)
		
	return render(request, "signup.html", context)

def login(request):
	form = LoginForm(request.POST or None)

	context = {
		"form" : form,
		"title" : "Thank You"
	}

	if form.is_valid():
		# user=form.save(commit=False)
		username=form.cleaned_data.get('username')
		password=form.cleaned_data.get('password')
		# user.save()
		user = authenticate(username = username, password = password)
		if not user:
			raise ValidationError('User Not Found')
		auth_login(request, user)
		context = {
			"title" : "Thank You"
		}
	if request.user.is_authenticated():
		track=Track.objects.filter(user_id=request.user.id)

		'''print(track)

		form=TrackForm(request.POST or None)
		if form.is_valid():
			profile=form.save(commit=False)
			profile.User_id=request.user.id
			# Doj=form.cleaned_data.get
			profile.save()
			#https://api.railwayapi.com/v2/between/source/<stn code>/dest/<stn code>/date/<dd-mm-yyyy>/apikey/<apikey>/
		'''
		date_list=[]
		for i in track:
			day=i.date_of_journey.day
			month=i.date_of_journey.month
			year=i.date_of_journey.year
			if month<10:
				if day<10:
					date_list.append("0"+str(day)+"-"+"0"+str(month)+"-"+str(year))
				else:
					date_list.append(str(day)+"-"+"0"+str(month)+"-"+str(year))
			else:
				date_list.append(str(day)+"-"+str(month)+"-"+str(year))

		train_list=[]
		j=0
		for i in track:
			str1="https://api.railwayapi.com/v2/between/source/"+i.Source_stn_code+"/dest/"+i.destination_stn_code+"/date/"+date_list[j]+"/apikey/"+API_KEY+"/"
			#print(str1)
			# str1="https://api.railwayapi.com/v2/between/source/MZP/dest/KGP/date/26-03-2018/apikey/0jz5osnlw7/"
			response=urllib.request.urlopen(str1).read()
			jsonResponse = json.loads(response.decode('utf-8'))
			#print(jsonResponse)
			temp=[]
			for k in jsonResponse['trains']:
				temp.append(k['number'])
			train_list.append(temp)
			j=j+1
		print(train_list)
		# content=urllib.request.urlopen("https://api.railwayapi.com/v2/check-seat/train/18005/source/KGP/dest/SBP/date/30-03-2018/pref/SL/quota/GN/apikey/0jz5osnlw7/").read()
		# content=urllib.request.urlopen("https://api.railwayapi.com/v2/between/source/MZP/dest/KGP/date/26-03-2018/apikey/0jz5osnlw7/").read()
		# jsonResponse = json.loads(content.decode('utf-8'))
		x=0
		avail=[]
		for row in train_list:
			src=track[x].Source_stn_code
			dst=track[x].destination_stn_code
			dt=date_list[x]
			for train in row:
				str2="https://api.railwayapi.com/v2/check-seat/train/"+train+"/source/"+src+"/dest/"+dst+"/date/"+dt+"/pref/SL/quota/GN/apikey/"+API_KEY+"/"
				response=urllib.request.urlopen(str2).read()
				jsonResponse = json.loads(response.decode('utf-8'))
				#print(jsonResponse)
				if(str(jsonResponse['train']['number'])!='None'):
					avail.append({'train_number':jsonResponse['train']['number'],'Class' : jsonResponse['journey_class']['code'],
					'Destination' : jsonResponse['to_station']['code'],'Source' : jsonResponse['from_station']['code'],'quota' : jsonResponse['quota']['code'],
					'status':jsonResponse['availability'][0]['status'],'Date':jsonResponse['availability'][0]['date']} )
			x=x+1
		'''
		x=0
		for row in train_list:
			src=track[x].Source_stn_code
			dst=track[x].destination_stn_code
			dt=date_list[x]
			for train in row:
				str2="https://api.railwayapi.com/v2/check-seat/train/"+train+"/source/"+src+"/dest/"+dst+"/date/"+dt+"/pref/3A/quota/GN/apikey/"+API_KEY+"/"
				response=urllib.request.urlopen(str2).read()
				jsonResponse = json.loads(response.decode('utf-8'))
				#print(jsonResponse)
				if(str(jsonResponse['train']['number'])!='None'):
					avail.append({'train_number':jsonResponse['train']['number'],'Class' : jsonResponse['journey_class']['code'],
					'Destination' : jsonResponse['to_station']['code'],'Source' : jsonResponse['from_station']['code'],'quota' : jsonResponse['quota']['code'],
					'status':jsonResponse['availability'][0]['status'],'Date':jsonResponse['availability'][0]['date']} )
			x=x+1

		x=0
		for row in train_list:
			src=track[x].Source_stn_code
			dst=track[x].destination_stn_code
			dt=date_list[x]
			for train in row:
				str2="https://api.railwayapi.com/v2/check-seat/train/"+train+"/source/"+src+"/dest/"+dst+"/date/"+dt+"/pref/2A/quota/GN/apikey/"+API_KEY+"/"
				response=urllib.request.urlopen(str2).read()
				jsonResponse = json.loads(response.decode('utf-8'))
				#print(jsonResponse)
				if(str(jsonResponse['train']['number'])!='None'):
					avail.append({'train_number':jsonResponse['train']['number'],'Class' : jsonResponse['journey_class']['code'],
					'Destination' : jsonResponse['to_station']['code'],'Source' : jsonResponse['from_station']['code'],'quota' : jsonResponse['quota']['code'],
					'status':jsonResponse['availability'][0]['status'],'Date':jsonResponse['availability'][0]['date']} )
			x=x+1

		x=0
		for row in train_list:
			src=track[x].Source_stn_code
			dst=track[x].destination_stn_code
			dt=date_list[x]
			for train in row:
				str2="https://api.railwayapi.com/v2/check-seat/train/"+train+"/source/"+src+"/dest/"+dst+"/date/"+dt+"/pref/1A/quota/GN/apikey/"+API_KEY+"/"
				response=urllib.request.urlopen(str2).read()
				jsonResponse = json.loads(response.decode('utf-8'))
				#print(jsonResponse)
				if(str(jsonResponse['train']['number'])!='None'):
					avail.append({'train_number':jsonResponse['train']['number'],'Class' : jsonResponse['journey_class']['code'],
					'Destination' : jsonResponse['to_station']['code'],'Source' : jsonResponse['from_station']['code'],'quota' : jsonResponse['quota']['code'],
					'status':jsonResponse['availability'][0]['status'],'Date':jsonResponse['availability'][0]['date']} )
			x=x+1

		x=0
		for row in train_list:
			src=track[x].Source_stn_code
			dst=track[x].destination_stn_code
			dt=date_list[x]
			for train in row:
				str2="https://api.railwayapi.com/v2/check-seat/train/"+train+"/source/"+src+"/dest/"+dst+"/date/"+dt+"/pref/FC/quota/GN/apikey/"+API_KEY+"/"
				response=urllib.request.urlopen(str2).read()
				jsonResponse = json.loads(response.decode('utf-8'))
				#print(jsonResponse)
				if(str(jsonResponse['train']['number'])!='None'):
					avail.append({'train_number':jsonResponse['train']['number'],'Class' : jsonResponse['journey_class']['code'],
					'Destination' : jsonResponse['to_station']['code'],'Source' : jsonResponse['from_station']['code'],'quota' : jsonResponse['quota']['code'],
					'status':jsonResponse['availability'][0]['status'],'Date':jsonResponse['availability'][0]['date']} )
			x=x+1

		x=0
		for row in train_list:
			src=track[x].Source_stn_code
			dst=track[x].destination_stn_code
			dt=date_list[x]
			for train in row:
				str2="https://api.railwayapi.com/v2/check-seat/train/"+train+"/source/"+src+"/dest/"+dst+"/date/"+dt+"/pref/CC/quota/GN/apikey/"+API_KEY+"/"
				response=urllib.request.urlopen(str2).read()
				jsonResponse = json.loads(response.decode('utf-8'))
				#print(jsonResponse)
				if(str(jsonResponse['train']['number'])!='None'):
					avail.append({'train_number':jsonResponse['train']['number'],'Class' : jsonResponse['journey_class']['code'],
					'Destination' : jsonResponse['to_station']['code'],'Source' : jsonResponse['from_station']['code'],'quota' : jsonResponse['quota']['code'],
					'status':jsonResponse['availability'][0]['status'],'Date':jsonResponse['availability'][0]['date']} )
			x=x+1

		x=0
		for row in train_list:
			src=track[x].Source_stn_code
			dst=track[x].destination_stn_code
			dt=date_list[x]
			for train in row:
				str2="https://api.railwayapi.com/v2/check-seat/train/"+train+"/source/"+src+"/dest/"+dst+"/date/"+dt+"/pref/2S/quota/GN/apikey/"+API_KEY+"/"
				response=urllib.request.urlopen(str2).read()
				jsonResponse = json.loads(response.decode('utf-8'))
				#print(jsonResponse)
				if(str(jsonResponse['train']['number'])!='None'):
					avail.append({'train_number':jsonResponse['train']['number'],'Class' : jsonResponse['journey_class']['code'],
					'Destination' : jsonResponse['to_station']['code'],'Source' : jsonResponse['from_station']['code'],'quota' : jsonResponse['quota']['code'],
					'status':jsonResponse['availability'][0]['status'],'Date':jsonResponse['availability'][0]['date']} )
			x=x+1
		'''	
		context={
		"content":avail,
		#"form":form,
		# "track":ret_list,
		# "track":track[0].date_of_journey,
		}
		return render(request,'new.html',context)
	if not request.user.id:
		request.user.id=0

	return render(request, "login.html", context)

def track(request):
	form = TrackForm(request.POST or None)
	context = {
		"title" : "We will keep you updated!! ",
		"form" : form
	}
	if form.is_valid():
		profile = form.save(commit=False)
		profile.user_id = request.user.id
		profile.save()
		context = {
			"title" : "Thanks!! ",
		}
		return render(request, "main.html",context)
	 
	return render(request, "track.html",context)

def myData(request):
	form = myDataForm(request.POST or None)
	context = {
		"title" : "We will keep you updated!! ",
		"form" : form
	}
	if form.is_valid():
		profile = form.save(commit=False)
		profile.User_id = request.user.id
		profile.save()
		context = {
			"title" : "Thanks!! ",
		}
		# form.save()
		return render(request, "main.html",context)
	 
	return render(request, "myData.html",context)

def ShowStatus(request):
	track=Tracker.objects.filter(User_id=request.user.id).order_by("-Created_at")

	print(track)
	form=TrackerForm(request.POST or None)
	if form.is_valid():
		profile=form.save(commit=False)
		profile.User_id=request.user.id
		# Doj=form.cleaned_data.get
		profile.save()
		#https://api.railwayapi.com/v2/between/source/<stn code>/dest/<stn code>/date/<dd-mm-yyyy>/apikey/<apikey>/
	
	date_list=[]
	for i in track:
		day=i.date_of_journey.day
		month=i.date_of_journey.month
		year=i.date_of_journey.year
		if month<10:
			if day<10:
				date_list.append("0"+str(day)+"-"+"0"+str(month)+"-"+str(year))
			else:
				date_list.append(str(day)+"-"+"0"+str(month)+"-"+str(year))
		else:
			date_list.append(str(day)+"-"+str(month)+"-"+str(year))

	train_list=[]
	j=0
	for i in track:
		str1="https://api.railwayapi.com/v2/between/source/"+i.Source_stn_code+"/dest/"+i.destination_stn_code+"/date/"+date_list[j]+"/apikey/"+API_KEY+"/"
		#print(str1)
		# str1="https://api.railwayapi.com/v2/between/source/MZP/dest/KGP/date/26-03-2018/apikey/0jz5osnlw7/"
		response=urllib.request.urlopen(str1).read()
		jsonResponse = json.loads(response.decode('utf-8'))
		#print(jsonResponse)
		temp=[]
		for k in jsonResponse['trains']:
			temp.append(k['number'])
		train_list.append(temp)
		j=j+1
	print(train_list)
	# content=urllib.request.urlopen("https://api.railwayapi.com/v2/check-seat/train/18005/source/KGP/dest/SBP/date/30-03-2018/pref/SL/quota/GN/apikey/0jz5osnlw7/").read()
	# content=urllib.request.urlopen("https://api.railwayapi.com/v2/between/source/MZP/dest/KGP/date/26-03-2018/apikey/0jz5osnlw7/").read()
	# jsonResponse = json.loads(content.decode('utf-8'))
	x=0
	avail=[]
	for row in train_list:
		src=track[x].Source_stn_code
		dst=track[x].destination_stn_code
		dt=date_list[x]
		for train in row:
			str2="https://api.railwayapi.com/v2/check-seat/train/"+train+"/source/"+src+"/dest/"+dst+"/date/"+dt+"/pref/SL/quota/GN/apikey/"+API_KEY+"/"
			response=urllib.request.urlopen(str2).read()
			jsonResponse = json.loads(response.decode('utf-8'))
			#print(jsonResponse)
			if(str(jsonResponse['train']['number'])!='None'):
				avail.append({'train_number':jsonResponse['train']['number'],'Class' : jsonResponse['journey_class']['code'],
				'Destination' : jsonResponse['to_station']['code'],'Source' : jsonResponse['from_station']['code'],'quota' : jsonResponse['quota']['code'],
				'status':jsonResponse['availability'][0]['status'],'Date':jsonResponse['availability'][0]['date']} )
		x=x+1

	x=0
	for row in train_list:
		src=track[x].Source_stn_code
		dst=track[x].destination_stn_code
		dt=date_list[x]
		for train in row:
			str2="https://api.railwayapi.com/v2/check-seat/train/"+train+"/source/"+src+"/dest/"+dst+"/date/"+dt+"/pref/3A/quota/GN/apikey/"+API_KEY+"/"
			response=urllib.request.urlopen(str2).read()
			jsonResponse = json.loads(response.decode('utf-8'))
			#print(jsonResponse)
			if(str(jsonResponse['train']['number'])!='None'):
				avail.append({'train_number':jsonResponse['train']['number'],'Class' : jsonResponse['journey_class']['code'],
				'Destination' : jsonResponse['to_station']['code'],'Source' : jsonResponse['from_station']['code'],'quota' : jsonResponse['quota']['code'],
				'status':jsonResponse['availability'][0]['status'],'Date':jsonResponse['availability'][0]['date']} )
		x=x+1

	x=0
	for row in train_list:
		src=track[x].Source_stn_code
		dst=track[x].destination_stn_code
		dt=date_list[x]
		for train in row:
			str2="https://api.railwayapi.com/v2/check-seat/train/"+train+"/source/"+src+"/dest/"+dst+"/date/"+dt+"/pref/2A/quota/GN/apikey/"+API_KEY+"/"
			response=urllib.request.urlopen(str2).read()
			jsonResponse = json.loads(response.decode('utf-8'))
			#print(jsonResponse)
			if(str(jsonResponse['train']['number'])!='None'):
				avail.append({'train_number':jsonResponse['train']['number'],'Class' : jsonResponse['journey_class']['code'],
				'Destination' : jsonResponse['to_station']['code'],'Source' : jsonResponse['from_station']['code'],'quota' : jsonResponse['quota']['code'],
				'status':jsonResponse['availability'][0]['status'],'Date':jsonResponse['availability'][0]['date']} )
		x=x+1

	x=0
	for row in train_list:
		src=track[x].Source_stn_code
		dst=track[x].destination_stn_code
		dt=date_list[x]
		for train in row:
			str2="https://api.railwayapi.com/v2/check-seat/train/"+train+"/source/"+src+"/dest/"+dst+"/date/"+dt+"/pref/1A/quota/GN/apikey/"+API_KEY+"/"
			response=urllib.request.urlopen(str2).read()
			jsonResponse = json.loads(response.decode('utf-8'))
			#print(jsonResponse)
			if(str(jsonResponse['train']['number'])!='None'):
				avail.append({'train_number':jsonResponse['train']['number'],'Class' : jsonResponse['journey_class']['code'],
				'Destination' : jsonResponse['to_station']['code'],'Source' : jsonResponse['from_station']['code'],'quota' : jsonResponse['quota']['code'],
				'status':jsonResponse['availability'][0]['status'],'Date':jsonResponse['availability'][0]['date']} )
		x=x+1

	x=0
	for row in train_list:
		src=track[x].Source_stn_code
		dst=track[x].destination_stn_code
		dt=date_list[x]
		for train in row:
			str2="https://api.railwayapi.com/v2/check-seat/train/"+train+"/source/"+src+"/dest/"+dst+"/date/"+dt+"/pref/FC/quota/GN/apikey/"+API_KEY+"/"
			response=urllib.request.urlopen(str2).read()
			jsonResponse = json.loads(response.decode('utf-8'))
			#print(jsonResponse)
			if(str(jsonResponse['train']['number'])!='None'):
				avail.append({'train_number':jsonResponse['train']['number'],'Class' : jsonResponse['journey_class']['code'],
				'Destination' : jsonResponse['to_station']['code'],'Source' : jsonResponse['from_station']['code'],'quota' : jsonResponse['quota']['code'],
				'status':jsonResponse['availability'][0]['status'],'Date':jsonResponse['availability'][0]['date']} )
		x=x+1

	x=0
	for row in train_list:
		src=track[x].Source_stn_code
		dst=track[x].destination_stn_code
		dt=date_list[x]
		for train in row:
			str2="https://api.railwayapi.com/v2/check-seat/train/"+train+"/source/"+src+"/dest/"+dst+"/date/"+dt+"/pref/CC/quota/GN/apikey/"+API_KEY+"/"
			response=urllib.request.urlopen(str2).read()
			jsonResponse = json.loads(response.decode('utf-8'))
			#print(jsonResponse)
			if(str(jsonResponse['train']['number'])!='None'):
				avail.append({'train_number':jsonResponse['train']['number'],'Class' : jsonResponse['journey_class']['code'],
				'Destination' : jsonResponse['to_station']['code'],'Source' : jsonResponse['from_station']['code'],'quota' : jsonResponse['quota']['code'],
				'status':jsonResponse['availability'][0]['status'],'Date':jsonResponse['availability'][0]['date']} )
		x=x+1

	x=0
	for row in train_list:
		src=track[x].Source_stn_code
		dst=track[x].destination_stn_code
		dt=date_list[x]
		for train in row:
			str2="https://api.railwayapi.com/v2/check-seat/train/"+train+"/source/"+src+"/dest/"+dst+"/date/"+dt+"/pref/2S/quota/GN/apikey/"+API_KEY+"/"
			response=urllib.request.urlopen(str2).read()
			jsonResponse = json.loads(response.decode('utf-8'))
			#print(jsonResponse)
			if(str(jsonResponse['train']['number'])!='None'):
				avail.append({'train_number':jsonResponse['train']['number'],'Class' : jsonResponse['journey_class']['code'],
				'Destination' : jsonResponse['to_station']['code'],'Source' : jsonResponse['from_station']['code'],'quota' : jsonResponse['quota']['code'],
				'status':jsonResponse['availability'][0]['status'],'Date':jsonResponse['availability'][0]['date']} )
		x=x+1
		
	context={
	"content":avail,
	"form":form,
	# "track":ret_list,
	# "track":track[0].date_of_journey,
	}
	return render(request,'new.html',context)
	if not request.user.id:
		request.user.id=0



