from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from base.models import BaseModel
from users.models import User

# Create your models here.


class Evangelism(BaseModel):
    class FieldOptions(models.TextChoices):
        PREACHER = "PR", _("Preacher")
        PROPHECY = "P", _("Prophecy")
        MEDICAL = "M", _("Medical")
        PERSONAL = "PE", _("Personal Evangelism")
        CHILD = "CH", _("Child Evangelism")
        SONG = "SO", _("Song Evangelism")
        CITY = "C", _("City Evangelism")
        DISABLED = "D", _("Disability Evangelism")
        SPECIAL = "S", _("Special Classes Evangelism")
        BIBLESTUDY = "BS", _("Bible Study Evangelism")
        PUBLISHING = "PU", _("Publishing Evangelism")
        LAY = "L", _("Lay Evangelism")

    class EventSermonOption(models.TextChoices):
        SERMON = "S", _("Sermon")
        EVENT = "E", _("Event")

    class EventOptions(models.TextChoices):
        HEALTHEXPO = "HE", _("Health Expo")
        PERSONAL = "P", _("Personal")
        PUBLIC = "PU", _("Public Effort")
        MEETING = "M", _("Hall Meetings")
        LIVESTREAM = "L", _("Live Streaming")
        RECORDED = "R", _("Recorded Message")
        MATERIAL = "MD", _("Printed Material Distribution")

    field = models.CharField(
        max_length=50,
        choices=FieldOptions.choices,
        default=FieldOptions.PERSONAL,
        null=True,
        blank=True,
    )
    is_event = models.CharField(
        max_length=50,
        choices=EventSermonOption.choices,
        default=EventSermonOption.SERMON,
    )
    event = models.CharField(
        max_length=50,
        choices=EventOptions.choices,
        default=EventOptions.PERSONAL,
        null=True,
        blank=True,
    )
    event_name = models.TextField(max_length=1024, null=True, blank=True)
    event_date = models.DateTimeField(null=True, blank=True)
    event_location = models.CharField(max_length=255, null=True, blank=True)
    event_purpose = models.TextField(null=True, blank=True)
    event_duration = models.CharField(max_length=1024, null=True, blank=True)
    sermon_theme = models.TextField(null=True, blank=True)
    sermon_length = models.IntegerField(null=True, blank=True)
    number_attendees = models.IntegerField(null=True, blank=True)
    completed = models.BooleanField(default=False, null=True, blank=True)
    budget = models.FloatField(null=True, blank=True)
    number_converts = models.IntegerField(null=True, blank=True)
    number_followups = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.field


class Referees(BaseModel):
    name = models.CharField(max_length=1024, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = PhoneNumberField()


class Member(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=1024)
    password2 = models.CharField(max_length=1024, verbose_name="Confirm Password")
    conference_name = models.CharField(max_length=255)
    home_church_name = models.TextField()
    home_church_email = models.EmailField(max_length=254)
    home_church_phone_numbers = PhoneNumberField()
    home_church_location = models.CharField(max_length=50)
    church_elder_name = models.CharField(max_length=50)
    church_elder_email = models.EmailField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    occupation = models.CharField(max_length=255)
    baptized = models.BooleanField(default=True)
    position_church = models.CharField(max_length=255)


class Minister(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=1024)
    password2 = models.CharField(max_length=1024, verbose_name="Confirm Password")
    available = models.BooleanField(default=False)
    contact_assistant_name = models.CharField(max_length=255)
    contact_assistant_email = models.EmailField()
    conference_name = models.CharField(max_length=255)
    fields = models.ManyToManyField(Evangelism, blank=True, null=True)
    home_church_name = models.TextField()
    home_church_email = models.EmailField(max_length=254)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    home_church_phone_numbers = PhoneNumberField()
    home_church_location = models.CharField(max_length=50)
    church_elder_name = models.CharField(max_length=50)
    church_elder_email = models.EmailField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Ministry(BaseModel):
    class TypeOptions(models.TextChoices):
        INDEPENDENT = "I", _("Self Supporting")
        CHURCHBASED = "C", _("Supported Church")

    name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=1024)
    password2 = models.CharField(max_length=1024, verbose_name="Confirm Password")
    location = models.CharField(max_length=255)
    phone_numbers = PhoneNumberField()
    category = models.CharField(
        max_length=50, choices=TypeOptions.choices, default=TypeOptions.INDEPENDENT
    )
    conference_name = models.CharField(max_length=255)
    fields = models.ManyToManyField(Evangelism, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
