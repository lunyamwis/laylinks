from django.contrib import admin
from .models import Payment

# Register your models here.


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('variant', 'total', 'payment_purpose')


admin.site.register(Payment, PaymentAdmin)
