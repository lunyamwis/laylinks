from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from payment.models import Payment
from donation.forms import DonationForm, SubscriptionForm


def index(request):
    return render(request, 'base/index.html')


def subscription(request):
    if request.method == 'POST':
        f = SubscriptionForm(request.POST)
        if f.is_valid():
            request.session['subscription_plan'] = request.POST.get('plans')
            return redirect('donation:charge')
    else:
        f = SubscriptionForm()
    return render(request, 'base/subscription_form.html', locals())


def charge(request):

    subscription_plan = request.session.get('subscription_plan')
    host = request.get_host()
    payment = Payment()
    payment.variant = 'Paypal'
    if subscription_plan == '1-month':
        payment.total = 10
        payment.payment_purpose = 'D'
        price = "10"
        billing_cycle = 1
        billing_cycle_unit = "M"
    elif subscription_plan == '6-month':
        payment.total = 50
        payment.payment_purpose = 'D'
        price = "50"
        billing_cycle = 6
        billing_cycle_unit = "M"
    else:
        payment.total = 90
        payment.payment_purpose = 'D'
        price = "90"
        billing_cycle = 1
        billing_cycle_unit = "Y"

    payment.save()

    return redirect("payment:payment_details", payment_id=payment.id)


def donation(request):
    if request.method == 'POST':
        f = DonationForm(request.POST)
        if f.is_valid():
            request.session['one_time_amount'] = request.POST.get(
                'one_time_amount')
            return redirect('donation:charge_donation')
    else:
        f = DonationForm()
    return render(request, 'base/subscription_form.html', locals())


def charge_donation(request):

    donation_amount = request.session.get('one_time_amount')
    payment = Payment()
    payment.variant = 'Paypal'
    payment.total = donation_amount
    payment.payment_purpose = 'D'
    payment.save()

    return redirect("payment:payment_details", payment_id=payment.id)


def successMsg(request, args):
    amount = args
    return render(request, 'base/success.html', {'amount': amount})


def cancel(request):
    return render(request, 'base/cancel.html')
