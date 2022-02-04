from django import forms
from requests.exceptions import HTTPError

from .. import PaymentStatus
from ..core import get_credit_card_issuer
from ..forms import PaymentForm


class MpesaPaymentForm(PaymentForm):

    mobile_number = forms.CharField(label="Mobile Number", max_length=255)
