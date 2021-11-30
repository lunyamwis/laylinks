from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect, render
from payments import RedirectNeeded, get_payment_model
from rest_framework.views import APIView
from rest_framework.response import Response
import stripe

from content.models import Pricing

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def webhook(request):
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    payload = request.body

    # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
    signature = request.META["HTTP_STRIPE_SIGNATURE"]
    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=signature, secret=webhook_secret)
        data = event['data']
    except Exception as e:
        return e

    # Get the type of webhook event sent - used to check the status of PaymentIntents.
    event_type = event['type']
    data_object = data['object']

    if event_type == 'invoice.paid':
        # Used to provision services after the trial has ended.
        # The status of the invoice will show up as paid. Store the status in your
        # database to reference when a user accesses your service to avoid hitting rate
        # limits.
        # TODO: change the users subscription and pricing

        webhook_object = data["object"]
        stripe_customer_id = webhook_object["customer"]

        stripe_sub = stripe.Subscription.retrieve(
            webhook_object["subscription"])
        stripe_price_id = stripe_sub["plan"]["id"]

        pricing = Pricing.objects.get(stripe_price_id=stripe_price_id)

        user = User.objects.get(stripe_customer_id=stripe_customer_id)
        user.subscription.status = stripe_sub["status"]
        user.subscription.stripe_subscription_id = webhook_object["subscription"]
        user.subscription.pricing = pricing
        user.subscription.save()

    if event_type == 'invoice.finalized':
        # If you want to manually send out invoices to your customers
        # or store them locally to reference to avoid hitting Stripe rate limits.
        print(data)

    if event_type == 'customer.subscription.deleted':
        # handle subscription cancelled automatically based
        # upon your subscription settings. Or if the user cancels it.
        webhook_object = data["object"]
        stripe_customer_id = webhook_object["customer"]
        stripe_sub = stripe.Subscription.retrieve(webhook_object["id"])
        user = User.objects.get(stripe_customer_id=stripe_customer_id)
        user.subscription.status = stripe_sub["status"]
        user.subscription.save()

    if event_type == 'customer.subscription.trial_will_end':
        # Send notification to your user that the trial will end
        print(data)

    if event_type == 'customer.subscription.updated':
        print(data)

    return HttpResponse()


class EnrollView(generic.TemplateView):
    template_name = "payment/enroll.html"


def PaymentView(request, slug):
    subscription = request.user.subscription
    pricing = get_object_or_404(Pricing, slug=slug)

    if subscription.pricing == pricing and subscription.is_active:
        messages.info(request, "You are already enrolled for this package")
        return redirect("payment:enroll")

    context = {
        "pricing_tier": pricing,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
    }

    if subscription.is_active and subscription.pricing.stripe_price_id != "django-free-trial":
        return render(request, "payment/change.html", context)

    return render(request, "payment/checkout.html", context)


class CreateSubscriptionView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        customer_id = request.user.stripe_customer_id
        try:
            # Attach the payment method to the customer
            stripe.PaymentMethod.attach(
                data['paymentMethodId'],
                customer=customer_id,
            )
            # Set the default payment method on the customer
            stripe.Customer.modify(
                customer_id,
                invoice_settings={
                    'default_payment_method': data['paymentMethodId'],
                },
            )

            # Create the subscription
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{'price': data["priceId"]}],
                expand=['latest_invoice.payment_intent'],
            )

            data = {}
            data.update(subscription)

            return Response(data)
        except Exception as e:
            return Response({
                "error": {'message': str(e)}
            })


class RetryInvoiceView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        customer_id = request.user.stripe_customer_id
        try:

            stripe.PaymentMethod.attach(
                data['paymentMethodId'],
                customer=customer_id,
            )
            # Set the default payment method on the customer
            stripe.Customer.modify(
                customer_id,
                invoice_settings={
                    'default_payment_method': data['paymentMethodId'],
                },
            )

            invoice = stripe.Invoice.retrieve(
                data['invoiceId'],
                expand=['payment_intent'],
            )
            data = {}
            data.update(invoice)

            return Response(data)
        except Exception as e:

            return Response({
                "error": {'message': str(e)}
            })


class ChangeSubscriptionView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        subscription_id = request.user.subscription.stripe_subscription_id
        subscription = stripe.Subscription.retrieve(subscription_id)
        try:
            updatedSubscription = stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=False,
                items=[{
                    'id': subscription['items']['data'][0].id,
                    'price': request.data["priceId"],
                }],
                proration_behavior="always_invoice"
            )

            data = {}
            data.update(updatedSubscription)
            return Response(data)
        except Exception as e:
            return Response({
                "error": {'message': str(e)}
            })


def payment_details(request, payment_id):
    payment = get_object_or_404(get_payment_model(), id=payment_id)

    # request.POST['variant'] = payment.variant
    # request.POST['status'] = payment.status
    # request.POST['variant'] = payment.variant
    # request.POST['fraud_check'] = payment.fraud_check
    # request.POST['currency'] = payment.currency
    # request.POST['total'] = payment.total
    # request.POST['delivery'] = payment.delivery
    # request.POST['tax'] = payment.tax
    # request.POST['captured_amount'] = payment.captured_amount
    data = {}
    data['variant'] = payment.variant
    data['status'] = payment.status
    data['variant'] = payment.variant
    data['fraud_check'] = payment.fraud_status
    data['currency'] = payment.currency
    data['total'] = payment.total
    data['delivery'] = payment.delivery
    data['tax'] = payment.tax
    data['captured_amount'] = payment.captured_amount

    try:
        form = payment.get_form(data=data or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))
    return TemplateResponse(request, 'payment_forms/payment.html', {
        'form': form, 'payment': payment
    })
