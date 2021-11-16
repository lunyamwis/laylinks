from django.urls import path
from . import views

app_name = "donation"

urlpatterns = [
    path('', views.index, name="index"),
    path('donate/', views.donation, name='donation'),
    path('subscribe/', views.subscription, name='subscription'),
    path('charge/', views.charge, name="charge"),
    path('charge_donation/', views.charge_donation, name="charge_donation"),
    path('success/<str:args>/', views.successMsg, name="success"),
    path('cancel/', views.cancel, name="cancel")
]
