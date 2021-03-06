import datetime
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
            return HttpResponseRedirect('/all_songs')
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
            return HttpResponseRedirect("/all_songs")
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
                    return HttpResponseRedirect('/all_songs')
                except Member.DoesNotExist:
                    # this can only happen in case of admin/special user who did not create a user through the app
                    messages.error(request,"Some Error Ocurred")
                    return render(request,"index_page.html", {})
            else:
                messages.error(request,"Invalid email-password combination")
                return render(request,"index_page.html", {})

@login_required
def all_songs(request):
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

def member_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def shared_playlists(request):
    user = request.user
    member = Member.objects.get(user=user)
    if request.method == 'GET':
        playlists= list(Playlist.objects.filter(shareable=True))
        shared_by = []
        for i in playlists:
            if i.member==member:
                shared_by.append("You")
            else:
                shared_by.append(i.member.name)
        playlists=zip(playlists,shared_by)
        return render(request,"shared_playlists.html",{'member': member, 'playlists': playlists})
    # have to write something for POST request

#this is the clone API.
@login_required
def clone_playlist(request):
    user=request.user
    member = Member.objects.get(user=user)
    id = request.GET["id"]
    try:
        playlist = Playlist.objects.get(id=id)
    except:
        return HttpResponse("Some error ocurred")
    if playlist.shareable ==False:
        return HttpResponse("You are not authorised for cloning")
    p=Playlist.objects.filter(clone_text=playlist.clone_text,member=member)
    if len(p)>0:
        return HttpResponse("Playlist has already been cloned")
    else:
        new_playlist= Playlist(clone_text=playlist.clone_text,name=playlist.name,shareable=False,member=member)
        new_playlist.save()
        p2s = P2S.objects.filter(playlist=playlist)
        for i in p2s:
            j=P2S(song=i.song,playlist=new_playlist)
            j.save()
        return HttpResponse("Playlist is successfully cloned to your profile. Open My Playlists to see changes")

@login_required
def create_playlist(request):
    user = request.user
    member = Member.objects.get(user=user)
    if request.method == 'GET':
        songs = Song.objects.order_by('-votes')
        return render(request,'create_playlist.html',{'songs': songs, 'is_edit': False})

    if request.method == 'POST':
        songs=request.POST.getlist('songs')
        name = request.POST["name"]
        shareable = request.POST.get("shareable",False)
        if shareable : shareable=True
        clone_text = str(datetime.datetime.now()) + member.name
        #clone text will ensure that you can clone a playlist only once. further code details in clone_playlist() method
        playlist = Playlist(shareable=shareable,name=name,member=member,clone_text=clone_text)
        playlist.save()

        for i in songs:
            s=Song.objects.get(id=i)
            p2s = P2S(playlist=playlist,song=s)
            p2s.save()
        messages.success(request,"playlist created successfully")
        return HttpResponseRedirect("/my_playlists")

@login_required
def my_playlists(request):
    user=request.user
    member = Member.objects.get(user=user)
    playlists = Playlist.objects.filter(member=member)
    if len(playlists)==0:
        sz=True
    else:
        sz=False
    return render(request,"my_playlists.html",{'playlists': playlists, "member": member,'sz':sz})

#a person can only view a playlist if it either belongs to him or the playlist is public
@login_required
def view_playlist(request,id):
    try:
        playlist=Playlist.objects.get(id=id)
    except:
        messages.error(request,"No such playlist exists")
        return HttpResponseRedirect('/my_playlists')
    user=request.user
    member=Member.objects.get(user=user)
    if playlist.member!=member and playlist.shareable==False:
        messages.error(request,"You are not authorised to view the playlist")
        return HttpResponseRedirect('/my_playlists')
    p2s= (P2S.objects.filter(playlist=playlist))
    val = True if playlist.member==member else False
    songs=[]
    for i in p2s:
        songs.append(i.song)
    return render (request,"view_playlist.html",{'songs': songs,'val': val, 'id': id,'name': playlist.name})

#this function deletes a playlist. Should be a post request, but didnt feel the need to do that here
@login_required
def delete_playlist(request,id):
    try:
        playlist=Playlist.objects.get(id=id)
    except:
        messages.error(request,"No such playlist exists")
        return HttpResponseRedirect('/my_playlists')
    user=request.user
    member=Member.objects.get(user=user)
    if playlist.member!=member:
        messages.error(request,"You were not authorised for that operation")
    else:
        p2s=P2S.objects.filter(playlist=playlist)
        for i in p2s:
            i.delete()
        playlist.delete()
        messages.success(request,"Playlist Deleted Successfully")
        return HttpResponseRedirect("/my_playlists")

#this is for the rate api
@login_required
def rate(request):
    id=request.GET['id']
    playlist = Playlist.objects.get(id=id)
    val=request.GET['val']
    user=request.user
    member=Member.objects.get(user=user)
    val=int(val)
    rated = Rate.objects.filter(playlist=playlist,member=member)
    if len(rated)==0:
        playlist.rating =(( playlist.rating * playlist.users_rated)+val)/(playlist.users_rated+1)
        playlist.users_rated+=1
        playlist.save()
        rate = Rate(playlist=playlist,member=member,value=val)
        rate.save()
        return HttpResponse(str(playlist.rating))
    else:
        r=rated[0]
        playlist.rating = ((playlist.rating * playlist.users_rated) + val - r.value)/playlist.users_rated
        playlist.save()
        r.save()
        return HttpResponse(str(playlist.rating))

@login_required
def edit_playlist(request,id):
    user=request.user
    member=Member.objects.get(user=user)
    playlist = Playlist.objects.get(id=id)
    if request.method == 'GET':
        songs = Song.objects.order_by('-votes')
        return render(request,'create_playlist.html',{'songs': songs, 'is_edit': True, 'playlist': playlist})
    else:
        print (request.POST)
        name = request.POST["name"]
        shareable = request.POST.get("shareable",False)
        if shareable : shareable=True
        clone_text = str(datetime.datetime.now()) + member.name
        #clone text will ensure that you can clone a playlist only once. further code details in clone_playlist() method
        p2s = P2S.objects.filter(playlist=playlist)
        for i in p2s:
            i.delete()
        songs = request.POST.getlist('songs')
        playlist.shareable=shareable
        playlist.clone_text=clone_text
        playlist.name=name
        playlist.save()
        for i in songs:
            s=Song.objects.get(id=i)
            p2s = P2S(playlist=playlist,song=s)
            p2s.save()
        messages.success(request,"playlist edited successfully")
        return HttpResponseRedirect("/my_playlists")
