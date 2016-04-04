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
        #check if we are here for login or for registering
        if query=="register":
            fullname = request.POST["fullname"]
            email = (request.POST["email"])
            number = request.POST["number"]
            password = (request.POST["password"])
            confirm_password = request.POST["confirm_password"]
            username=email
            print (password)
            user=User(username=username,first_name=fullname,email=email,password=password)
            #add validations here or in the page js
            if User.objects.filter(username=username):
                messages.error(request, "User already registered")
                return render(request,"index_page.html", {})
            user.save()
            member=Member(user=user,name=fullname,email=email,number=number)
            member.save()
            user = authenticate(username=username,password=password)
            print (user)
            login(request,user)
            return HttpResponseRedirect("/playlist")
        #if the person filled the login form
        else:
            email=request.POST["email"]
            password=request.POST["password"]
            username=email
            user=authenticate(username=username,password=password)
            if user is not None:
                try:
                    member=Member.objects.get(user=user)
                    login(request,user)
                    return HttpResponseRedirect('/playlist')
                except Member.DoesNotExist:
                    # this can only happen in case of admin/special user who did not create a user through the app
                    messages.error(request,"Some Error Ocurred")
                    return render(request,"index_page.html", {})
            else:
                messages.error(request,"Invalid email-password combination")
                return render(request,"index_page.html", {})

@login_required
def playlist(request):
    return HttpResponse("the playlist")
