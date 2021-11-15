from django.urls import path
from .views import (
    member_registration,
    minister_registration,
    ministry_registration,
    field_registration
)

app_name = "evangelism"

urlpatterns = [
    path('member/create/', member_registration, name='member_registration'),
    path('minister/create/', minister_registration, name='minister_registration'),
    path('ministry/create/', ministry_registration, name='ministry_registration'),
    path('field/create/', field_registration, name='field_registration'),
]
