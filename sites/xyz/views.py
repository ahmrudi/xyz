# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse

# Create your views here.
def construction(request):
	return render(request, "construction/index.html")
	
def index(request):
	return HttpResponse("Test")
	
def change_password(request):
	if request.method == "POST":
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			return redirect('index')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'registration/change_password.html', {'form':form})