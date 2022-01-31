from django.urls import path, re_path

from evangelism.forms import (
    ChurchMemberDetailsForm, EvangelismForm, EventDetails, Logistics, MemberRegistrationForm,
    MinisterRegistrationForm, ChurchMinisterDetailsForm,
    ContactMinisterDetailsForm, SermonDetails, SurveyForm
)

from .views import (
    FieldListView,
    FieldRegistration,
    MemberRegistrationWizzard,
    MinisterRegistrationWizzard,
    MinistryListView,
    EvangelismWizzard,
    field_detail,
    member_registration,
    minister_registration,
    ministry_registration,
    field_registration,
    MinisterListView,
    MinisterDetailView,
    MinistryDetailView
)

app_name = "evangelism"

FORMS = (("member_details", MemberRegistrationForm),
         ("church_details", ChurchMemberDetailsForm))

MINISTRY_FORMS = [("minister_details", MinisterRegistrationForm),
                  ("church_details", ChurchMinisterDetailsForm),
                  ("contact_details", ContactMinisterDetailsForm)]

EVANGELISM_FORMS = [("field_details", EvangelismForm),
                    ("event_details", EventDetails),
                    ("sermon_details", SermonDetails),
                    ("logistic_details", Logistics),
                    ("survey_details", SurveyForm)]

# membership_wizzard = MemberRegistrationWizzard.as_view(
#     FORMS,
#     url_name='member_register_wizzard',
#     done_step_name='finished'
# )

# urlpatterns = [
#     re_path(r'^member/(?P<step>.+)/$',
#             membership_wizzard, name='member_register_wizzard'),
#     path('member/church_details', membership_wizzard, name='fin'),
# ]
urlpatterns = [
    path('member/register/', MemberRegistrationWizzard.as_view(
        FORMS), name='member_register_wizzard'),
    path('minister/register/', MinisterRegistrationWizzard.as_view(
        MINISTRY_FORMS), name='minister_register_wizzard'),
    path('field/invite/', EvangelismWizzard.as_view(
        EVANGELISM_FORMS), name='evangelism_wizzard'),
    path('member/create/', member_registration, name='member_registration'),
    path('minister/create/', minister_registration, name='minister_registration'),
    path('ministry/create/', ministry_registration, name='ministry_registration'),
    path('field/create/', field_registration, name='field_registration'),
    path("ministers/", MinisterListView.as_view(), name='ministers'),
    path("ministers/<int:pk>/", MinisterDetailView.as_view(), name='minister'),
    path("ministries/", MinistryListView.as_view(), name='ministries'),
    path("ministries/<int:pk>/", MinistryDetailView.as_view(), name='ministry'),
    path("fields/", FieldListView.as_view(), name='fields'),
    path("field/<str:name>/", field_detail, name='field'),
]
