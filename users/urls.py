from django.urls import path

from users.views import (
    UserProfile,
    user_detail_view,
    user_redirect_view,
    user_update_view,
    UserSubscriptionView,
    CancelSubscriptionView,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("<str:username>/subscription/",
         UserSubscriptionView.as_view(), name="subscription"),
    path("<str:username>/subscription/cancel/",
         CancelSubscriptionView.as_view(), name="cancel-subscription"),
    path("accounts/profile/", UserProfile.as_view(), name='user-profile'),

]
