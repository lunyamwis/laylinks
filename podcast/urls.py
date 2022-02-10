from django.urls import path

from . import views

app_name = "podcast"

urlpatterns = [
    path("list/", views.Channels.as_view(), name="list"),
    path("detail/<pk>/", views.ItemDetail.as_view(), name="detail"),
]
