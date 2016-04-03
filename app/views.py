from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.models import *

# Create your views here.
def index(request):
    user = request.user
    if user.is_authenticated():
        return HttpResponseRedirect('/playlist')
    return render(request, 'index_page.html', {})