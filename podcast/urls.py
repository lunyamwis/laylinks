from django.urls import path

from . import views

app_name = "podcast"

urlpatterns = [
    path("", views.ChannelList.as_view(), name="list"),
    path("<slug>/", views.ChannelDetail.as_view(), name="detail"),
    path("<slug:channel>/feed/", views.RSSFeed.as_view(), name="feed"),
    path("<slug:channel>/<slug:item>/", views.ItemDetail.as_view(), name="item"),
]
