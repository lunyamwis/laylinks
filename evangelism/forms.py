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

    class Meta:
        model = Member
        fields = ['conference_name', 'home_church_name',
                  'home_church_email', 'home_church_phone_numbers', 'church_elder_name']


class MinisterRegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = Minister
        fields = ['name', 'email', 'password', 'password2']


class ChurchMinisterDetailsForm(ModelForm):

    class Meta:
        model = Minister
        fields = ['conference_name', 'home_church_name',
                  'home_church_email', 'home_church_phone_numbers', 'church_elder_name', 'church_elder_email']


class ContactMinisterDetailsForm(ModelForm):

    class Meta:
        model = Minister
        fields = ['contact_assistant_name', 'contact_assistant_email']


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
        fields = [
            'field',
            'event',
        ]


class EventDetails(ModelForm):
    class Meta:
        model = Evangelism
        fields = [
            'event',
            'event_name',
            'event_date',
            'event_location',
            'event_purpose',
            'event_duration',
            'number_attendees'
        ]


class SermonDetails(ModelForm):
    class Meta:
        model = Evangelism
        fields = [
            'sermon_theme',
            'sermon_length',
        ]


class Logistics(ModelForm):
    class Meta:
        model = Evangelism
        fields = [
            'budget'
        ]


class SurveyForm(ModelForm):
    class Meta:
        model = Evangelism
        fields = [
            'number_converts',
            'number_followups'
        ]
