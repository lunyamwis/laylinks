from decimal import Decimal

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from payments import PurchasedItem
from payments.models import BasePayment

# Create your models here.


class Payment(BasePayment):
    class PurposeOptions(models.TextChoices):
        BUY = ("B", "Buy")
        DONATION = ("D", "Donation")
        COURSE = ("C", "Course")

    payment_purpose = models.CharField(
        max_length=255, choices=PurposeOptions.choices, default=PurposeOptions.BUY
    )
    mobile_number = PhoneNumberField(blank=True, null=True)
    mpesa_mobile_number = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.variant} - {self.billing_country_area}"

    def get_failure_url(self) -> str:
        return super().get_failure_url()

    def get_success_url(self) -> str:
        return super().get_success_url()

    def get_purchased_items(self):
        return super().get_purchased_items()

    def save(self, **kwargs):
        if self.mobile_number:
            self.mpesa_mobile_number = int(
                f"{self.mobile_number.country_code}{self.mobile_number.national_number}"
            )
        return super(Payment, self).save(**kwargs)
