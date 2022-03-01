"""
Date: 01/02/2022
Author: Martin Luther Bironga
Purpose: Evangelism Registration Forms
"""
from django import forms
from django.forms import ModelForm

from .models import Evangelism, Member, Minister, Ministry


class MemberRegistrationForm(ModelForm):
    """
    Collects Member Personal details
    """

    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        """
        Collects Member Personal details
        """

        model = Member
        fields = [
            "name",
            "email",
            "password",
            "password2",
            "occupation",
            "baptized",
            "position_church",
        ]

    def clean(self):
        """
        checks whether the passwords match
        """
        data = self.cleaned_data
        if data.get("password") != data.get("password2"):
            self.add_error("password2", "passwords do not match !")
        return data


class ChurchMemberDetailsForm(ModelForm):
    """
    Collects Church details
    """

    class Meta:
        """
        Collects Church details
        """

        model = Member
        fields = [
            "conference_name",
            "home_church_name",
            "home_church_email",
            "home_church_phone_numbers",
            "church_elder_name",
        ]


class MinisterRegistrationForm(ModelForm):
    """
    Collects Minister Personal details
    """

    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        """
        Collects Minister Personal details
        """

        model = Minister
        fields = ["name", "email", "password", "password2"]

    def clean(self):
        """
        checks whether the passwords match
        """
        data = self.cleaned_data
        if data.get("password") != data.get("password2"):
            self.add_error("password2", "passwords do not match !")
        return data


class ChurchMinisterDetailsForm(ModelForm):
    """
    Collects Minister Church details
    """

    class Meta:
        """
        Collects Minister Church details
        """

        model = Minister
        fields = [
            "conference_name",
            "home_church_name",
            "home_church_email",
            "home_church_phone_numbers",
            "church_elder_name",
            "church_elder_email",
        ]


class ContactMinisterDetailsForm(ModelForm):
    """
    Collects Minister Contact Info details
    """

    class Meta:
        """
        Collects Minister Contact Info details
        """

        model = Minister
        fields = ["contact_assistant_name", "contact_assistant_email"]


class MinistryRegistrationForm(ModelForm):
    """
    Collect Ministry Details
    """

    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        """
        Collect Ministry Details
        """

        model = Ministry
        exclude = ["user", "fields"]

    def clean(self):
        """
        checks whether the passwords match
        """
        data = self.cleaned_data
        if data.get("password") != data.get("password2"):
            self.add_error("password2", "passwords do not match !")
        return data


class EvangelismForm(ModelForm):
    """
    Collect Field Details
    """

    class Meta:
        """
        Collect Field Details
        """

        model = Evangelism
        fields = [
            "field",
            "is_event",
        ]


class EventDetails(ModelForm):
    """
    Collect Event Details
    """

    class Meta:
        """
        Collect Event Details
        """

        model = Evangelism
        fields = [
            "event",
            "event_name",
            "event_date",
            "event_location",
            "event_purpose",
            "event_duration",
            "number_attendees",
        ]


class SermonDetails(ModelForm):
    """
    Collect Sermon Details
    """

    class Meta:
        """
        Collect Sermon Details
        """

        model = Evangelism
        fields = [
            "sermon_theme",
            "sermon_length",
        ]


class Logistics(ModelForm):
    """
    Collect Logistic Details
    """

    class Meta:
        """
        Collect Logistic Details
        """

        model = Evangelism
        fields = ["budget"]


class SurveyForm(ModelForm):
    """
    Collect Survey of Event Details
    """

    class Meta:
        """
        Collect Survey of Event Details
        """

        model = Evangelism
        fields = ["number_converts", "number_followups"]
