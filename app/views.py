from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from app.forms import UploadSongForm
from app.models import *
import sys

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
            print (fullname,email,number,password,confirm_password)
            #add validations here or in the page js
            # TODO: Please not that validations have not been done
            if User.objects.filter(username=username):
                messages.error(request, "User already registered")
                return render(request,"index_page.html", {})
            if password!=confirm_password:
                messages.error(request,"The two passwords should match")
                return render(request,"index_page.html", {})
            if len(password)<8:
                messages.error(request,"Password is too short")
                return render(request,"index_page.html", {})
            user=User.objects.create_user(username=username,first_name=fullname,email=email,password=password)
            user.save()
            member=Member(user=user,name=fullname,email=email,number=number)
            member.save()
            user = authenticate(username=username,password=password)
            print (user)
            login(request,user)
            print ("heya")
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
    user = request.user
    member = Member.objects.get(user=user)
    #to upload a song. Note that for now, I am just allowing the user to upload in .mp3 format
    if request.method=="POST":
        # temp=request.POST.getlist("song")[0]
        form = UploadSongForm(request.POST,request.FILES)
        print (request.FILES)
        if form.is_valid():
            name=str(request.FILES["fi"])
            song = Song(name=name,file=form.cleaned_data["fi"],uploader=member)
            song.save()
    form = UploadSongForm()
    songs = Song.objects.order_by('-votes')
    votes=[]
    #this loop is to find out songs the particular user has already voted for
    for i in songs:
        s = M2SVote.objects.filter(song=i,member=member)
        if len(s)>0:
            votes.append(True)
        else:
            votes.append(False)
    songs = zip(songs,votes)
    # songs.sort(key=lambda x: x.votes,reverse=True)
    return render(request,"playlist.html",{"member": member, "songs": songs,'form': form})

#this function handles the upvote api.
@login_required
def upvote(request):
    user=request.user
    member = Member.objects.get(user=user)
    print (member)
    print (request.GET)
    id=request.GET["id"]
    val=request.GET["val"]
    print (val)
    #if you want to either upvote or downvote
    if val!="3":
        vote=M2SVote.objects.filter(song__id=id,member=member)
        if len(vote)>0:
            return # you have already cast a vote and are now trying to do something fishy
        else:
            song=Song.objects.get(id=id)
            vote=M2SVote(song=song,member=member)
            if val == "1":
                vote.upvote=True
                song.votes= song.votes+1
            else:
                vote.upvote=False
                song.votes=song.votes-1
            song.save()
            vote.save()
            return HttpResponse(str(song.votes))
    #if you want to cancel your previous vote
    else:
        song=Song.objects.get(id=id)
        vote=M2SVote.objects.get(song=song,member=member)
        if vote == None:
            return HttpResponse("Some Error Ocurred. Wrong request.")
        else:
            if vote.upvote==True:
                song.votes-=1
            else:
                song.votes+=1
            song.save()
            vote.delete()
            return HttpResponse(str(song.votes))