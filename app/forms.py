from django import forms
from django.forms import ModelForm

class UploadSongForm(forms.Form):
    fi=forms.FileField()