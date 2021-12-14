from django import forms
from django.forms import ModelForm
from django import forms
from .models import (Member, Minister, Ministry, Evangelism)


class MemberRegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Member
        exclude = ['user']


class MinisterRegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Minister
        exclude = ['user', 'fields']


class MinistryRegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Ministry
        exclude = ['user', 'fields']


class EvangelismForm(ModelForm):
    class Meta:
        model = Evangelism
        exclude = [
            'sermon_theme',
            'sermon_length',
            'number_attendees',
            'budget',
            'number_converts',
            'number_followups',
        ]
