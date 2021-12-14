from django.contrib import admin

from .models import Course, Video, Pricing, Subscription

admin.site.site_header = "Laylinks Admin"
admin.site.site_title = "Laylinks Admin Portal"
admin.site.index_title = "Welcome to the Laylinks Admin Portal"
admin.site.register(Course)
admin.site.register(Video)
admin.site.register(Pricing)
admin.site.register(Subscription)
