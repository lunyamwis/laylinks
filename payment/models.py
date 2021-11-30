from django.db import models
from decimal import Decimal

from payments import PurchasedItem
from payments.models import BasePayment

# Create your models here.


class Payment(BasePayment):

    def get_failure_url(self) -> str:
        return super().get_failure_url()

    def get_success_url(self) -> str:
        return super().get_success_url()

    def get_purchased_items(self):
        return super().get_purchased_items()
