"""
Date: 01/02/2022
Author: Martin Luther Bironga
Purpose: Routing the main urls
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from marketing.views import email_list_signup
from posts.views import (
    IndexView,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
    about,
    search,
)

# from djangojs.views import JasmineView, QUnitView

# urlpatterns = [
#     re_path('^jasmine$', JasmineView.as_view(
#         js_files='js/specs/*.specs.js'), name='my_jasmine_view'),
#     re_path('^qunit$', QUnitView.as_view(
#         js_files='js/tests/*.tests.js'), name='my_qunit_view'),
# ]
urlpatterns = [
    path("admin/", admin.site.urls),
    # path('', index),
    path("", IndexView.as_view(), name="home"),
    path("about/", about, name="about"),
    # path('blog/', post_list, name='post-list'),
    path("blog/", PostListView.as_view(), name="post-list"),
    path("search/", search, name="search"),
    path("email-signup/", email_list_signup, name="email-list-signup"),
    # path('create/', post_create, name='post-create'),
    path("create/", PostCreateView.as_view(), name="post-create"),
    # path('post/<id>/', post_detail, name='post-detail'),
    path("post/<pk>/", PostDetailView.as_view(), name="post-detail"),
    # path('post/<id>/update/', post_update, name='post-update'),
    path("post/<pk>/update/", PostUpdateView.as_view(), name="post-update"),
    # path('post/<id>/delete/', post_delete, name='post-delete'),
    path("post/<pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("tinymce/", include("tinymce.urls")),
    path("users/", include("users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path("courses/", include("content.urls")),
    path("shop/", include("shop.urls")),
    path("evangelism/", include("evangelism.urls", namespace="evangelism")),
    path("donation/", include("donation.urls", namespace="donation")),
    path("payment/", include("payment.urls")),
    path("payments/", include("payments.urls")),
    path("podcast/", include("podcast.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
