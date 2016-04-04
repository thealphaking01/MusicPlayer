from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.models import *

# We first check that if a user is already logged in. In case he isn't and he wants to register/login, we do the required.
def index(request):
    if request.method=="GET":
        user = request.user
        if user.is_authenticated():
            return HttpResponseRedirect('/playlist')
        return render(request, 'index_page.html', {})
    elif request.method=="POST":
        query = request.POST["check"]
        #how did the control arrive here? is the request for register or for login?
        if query=="register":
            fullname = request.POST["fullname"]
            email = request.POST["email"]
            number = request.POST["number"]
            password = request.POST["password"]
            confirm_password = request.POST["confirm_password"]
            username=email
            user=User(username=username,first_name=fullname,email=email,password=password)
            # member=
            if User.objects.filter(username=username):
                messages.error(request, "User already registered")
                return render(request,"index_page.html", {})
            user.save()
            # member.save()
            return HttpResponseRedirect("/playlist")
        #if the person filled the login form
        else:
            email=request.POST["email"]
            password=request.POST["password"]
            username=email
            user=authenticate(username=username,password=password)
            if user is not None:
                # member=Member.objects.get(user=user)
                # you also have to add a check if this query fails - say, for the admin
                # Member.DoesNotExist
                return HttpResponse("huhaha")
            else:
                messages.error(request,"Invalid email-password combination")
                return render(request,"index_page.html", {})





@login_required
def playlist(request):
    return HttpResponse("the playlist")
