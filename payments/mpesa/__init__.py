import json
import base64
import logging
from datetime import timedelta, datetime
from decimal import ROUND_HALF_UP
from decimal import Decimal
from functools import wraps

import requests
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils import timezone
from requests.exceptions import HTTPError

from .. import PaymentError
from .. import PaymentStatus
from .. import RedirectNeeded
from ..core import BasicProvider
from ..core import get_credit_card_issuer
from .forms import PaymentForm

# Get an instance of a logger
logger = logging.getLogger(__name__)

CENTS = Decimal("0.01")


class UnauthorizedRequest(Exception):
    pass


class MpesaProvider(BasicProvider):
    """Payment provider for Paypal, redirection-based.

    This backend implements payments using `PayPal.com <https://www.paypal.com/>`_.

    :param client_id: Client ID assigned by PayPal or your email address
    :param secret: Secret assigned by PayPal
    :param endpoint: The API endpoint to use. For the production environment, use ``'https://api.paypal.com'`` instead
    :param capture: Whether to capture the payment automatically. See :ref:`capture-payments` for more details.
    """

    def __init__(
        self,
        consumer_key,
        consumer_secret,
        business_short_code=174379,
        auth_endpoint="https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials",
        endpoint="https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        basic_token="U3FTOWdzRXJnVldvdmJHbWxEbXJJV2RKdkdXaThBYnk6amtQMU9EYkFvRUx4S0FEVQ==",
        passkey="bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919",
    ):
        self.consumer_secret = consumer_secret
        self.consumer_key = consumer_key
        self.auth_endpoint = auth_endpoint
        self.endpoint = endpoint
        self.business_short_code = business_short_code
        self.basic_token = basic_token
        self.timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.passkey = passkey

        super().__init__()

    def create_payment(self, payment, extra_data=None):
        product_data = self.get_product_data(payment, extra_data)
        payment = self.post(payment, self.payments_url, data=product_data)
        return payment

    def get_amount_data(self, payment, amount=None):
        return {
            "currency": payment.currency,
            "total": str(amount.quantize(CENTS, rounding=ROUND_HALF_UP)),
        }

    def get_form(self, payment, data=None):
        if payment.status == PaymentStatus.WAITING:
            payment.change_status(PaymentStatus.INPUT)
        form = PaymentForm(data, provider=self, payment=payment)
        if form.is_valid():
            raise RedirectNeeded(payment.get_success_url())
        return form

    def get_access_token(self):
        response = requests.request(
            "GET",
            self.auth_endpoint,
            headers={"Authorization": f"Basic {self.basic_token}"},
        )
        resp = response.json()
        return f"Bearer {resp['access_token']}"

    def generate_password(self):
        data_to_encode = f"{self.business_short_code}{self.passkey}{self.timestamp}"
        online_password = base64.b64encode(data_to_encode.encode())
        decode_password = online_password.decode("utf-8")
        return decode_password

    def post(self, payment):
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.get_access_token(),
        }
        payload = {
            "BusinessShortCode": self.business_short_code,
            "Password": self.generate_password(),
            "Timestamp": self.timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(payment.total),
            "PartyA": int(payment.mpesa_mobile_number),
            "PartyB": 174379,
            "PhoneNumber": int(payment.mpesa_mobile_number),
            "CallBackURL": "https://mydomain.com/path",
            "AccountReference": "CompanyXLTD",
            "TransactionDesc": "Payment of X",
        }
        response = requests.post(
            url=self.endpoint, headers=headers, data=json.dumps(payload)
        )
        try:
            data = response.json()
        except ValueError:
            data = {}
        return data
