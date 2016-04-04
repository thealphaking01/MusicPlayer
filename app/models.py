from django.db import models
from django.contrib.auth.models import User

from django.contrib import admin

# Create your models here.

class Member(models.Model):
    class Meta:
        db_table = 'member'

    user = models.OneToOneField(User)
    name = models.CharField(max_length=255,default="")
    email = models.CharField(max_length=255,default="")
    number = models.TextField(max_length=10,default="")

    def __str__(self):
        return "Name: " + str(self.name) + " Email : " + str(self.email)

class Song(models.Model):
    class Meta:
        db_table = 'song'

    name = models.TextField(max_length=255)
    file = models.FileField(default=None)
    uploader = models.ForeignKey(Member)
    votes = models.IntegerField(default=0)

class M2SVote(models.Model):
    class Meta:
        db_table = 'vote'

    song = models.ForeignKey(Song)
    member = models.ForeignKey(Member)
    # if the entry is present and upvote is false, this would mean that it is a downvote
    #if no entry is present, then the member/user hasn't voted yet
    upvote = models.BooleanField(default=False)

admin.site.register(Member)
admin.site.register(Song)
admin.site.register(M2SVote)