from django.urls import path
from .views import (
    FieldListView,
    MinistryListView,
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

urlpatterns = [
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
