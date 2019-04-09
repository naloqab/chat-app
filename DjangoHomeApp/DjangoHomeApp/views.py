from django.http import HttpResponse
import datetime
from django.urls import include
from django.shortcuts import render, redirect

def index(request):
	return render(request, 'index.html', context=None)