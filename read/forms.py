from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Feed, Publication

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = ["title", "description", "email_frequency"]

class SubForm(forms.Form):
    pubs = Publication.objects.all()
    OPTIONS = (
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
    )
    # for pub in pubs

    checkboxes = forms.MultipleChoiceField(choices=OPTIONS, widget=forms.CheckboxSelectMultiple)
