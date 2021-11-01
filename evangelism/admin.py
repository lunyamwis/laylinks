from django.contrib import admin
from .models import (Member,Ministry,Minister,Evangelism)
# Register your models here.
admin.site.register(Member)
admin.site.register(Minister)
admin.site.register(Ministry)
admin.site.register(Evangelism)