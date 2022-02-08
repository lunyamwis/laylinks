from django.urls import path

from . import views

app_name = "donation"

urlpatterns = [
    path("", views.index, name="index"),
    path("donate/", views.DonationView.as_view(), name="donation"),
    path("success/<str:args>/", views.successMsg, name="success"),
    path("cancel/", views.cancel, name="cancel"),
]
