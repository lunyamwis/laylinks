"""
Date: 01/02/2022
Author: Martin Luther Bironga
Purpose: Routing the evangelism view urls
"""
from django.urls import path

from evangelism.forms import (
    ChurchMemberDetailsForm,
    ChurchMinisterDetailsForm,
    ContactMinisterDetailsForm,
    EvangelismForm,
    EventDetails,
    Logistics,
    MemberRegistrationForm,
    MinisterRegistrationForm,
    MinistryRegistrationForm,
    SermonDetails,
    SurveyForm,
)

from .views import (
    EvangelismListView,
    EvangelismWizzard,
    MemberListView,
    MemberRegistrationWizzard,
    MinisterListView,
    MinisterRegistrationWizzard,
    MinistryListView,
    MinistryRegistrationWizzard,
    field_detail,
)

app_name = "evangelism"

FORMS = (
    ("member_details", MemberRegistrationForm),
    ("church_details", ChurchMemberDetailsForm),
)

MINISTER_FORMS = [
    ("minister_details", MinisterRegistrationForm),
    ("church_details", ChurchMinisterDetailsForm),
    ("contact_details", ContactMinisterDetailsForm),
]

EVANGELISM_FORMS = [
    ("field_details", EvangelismForm),
    ("event_details", EventDetails),
    ("sermon_details", SermonDetails),
    ("logistic_details", Logistics),
    ("survey_details", SurveyForm),
]

MINISTRY_FORMS = [("ministry_details", MinistryRegistrationForm)]


urlpatterns = [
    path(
        "member/register/",
        MemberRegistrationWizzard.as_view(FORMS),
        name="member_register_wizzard",
    ),
    path("member/list/", MemberListView.as_view(), name="member_list"),
    path(
        "minister/register/",
        MinisterRegistrationWizzard.as_view(MINISTER_FORMS),
        name="minister_register_wizzard",
    ),
    path("minister/list/", MinisterListView.as_view(), name="minister_list"),
    path(
        "ministry/register/",
        MinistryRegistrationWizzard.as_view(MINISTRY_FORMS),
        name="ministry_register_wizzard",
    ),
    path("ministry/list/", MinistryListView.as_view(), name="ministry_list"),
    path(
        "field/invite/",
        EvangelismWizzard.as_view(EVANGELISM_FORMS),
        name="evangelism_wizzard",
    ),
    path(
        "field/list/",
        EvangelismListView.as_view(),
        name="events_list",
    ),
    path("field/<str:name>/", field_detail, name="field"),
]
