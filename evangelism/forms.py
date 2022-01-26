from django import forms
from django.forms import ModelForm, fields
from django import forms
from .models import (Member, Minister, Ministry, Evangelism)


class MemberRegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = Member
        fields = ['name', 'password', 'password2',
                  'occupation', 'baptized', 'position_church']


class ChurchMemberDetailsForm(ModelForm):
    # conference_name = forms.CharField(max_length=255)
    # field_name = forms.CharField(max_length=255)
    # home_church_name = forms.TextField()
    # home_church_email = forms.EmailField(max_length=254)
    # home_church_phone_numbers = forms.CharField(max_length=200, null=True)
    # home_church_location = forms.CharField(max_length=50)
    # church_elder_name = forms.CharField(max_length=50)
    # church_elder_email = forms.EmailField(max_length=50)

    class Meta:
        model = Member
        fields = ['conference_name', 'field_name', 'home_church_name',
                  'home_church_email', 'home_church_phone_numbers', 'church_elder_name']


class MinisterRegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = Minister
        exclude = ['user', 'fields']


class MinistryRegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password")

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
