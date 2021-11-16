from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm

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

    if subscription_plan == '1-month':
        price = "10"
        billing_cycle = 1
        billing_cycle_unit = "M"
    elif subscription_plan == '6-month':
        price = "50"
        billing_cycle = 6
        billing_cycle_unit = "M"
    else:
        price = "90"
        billing_cycle = 1
        billing_cycle_unit = "Y"

    paypal_dict = {
        "cmd": "_xclick-subscriptions",
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        "a3": price,  # monthly price
        "p3": billing_cycle,  # duration of each unit (depends on unit)
        "t3": billing_cycle_unit,  # duration unit ("M for Month")
        "src": "1",  # make payments recur
        "sra": "1",  # reattempt payment on payment error
        "no_note": "1",  # remove extra notes (optional)
        'item_name': 'Content subscription',
        'custom': 1,     # custom data, pass something meaningful here
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           redirect('donation:success', price)),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('donation:cancel')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
    return render(request, 'base/index.html', locals())


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
    host = request.get_host()

    paypal_dict = {
        "cmd": "_xclick",
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': donation_amount,
        'item_name': 'Donate',
        'custom': 1,     # custom data, pass something meaningful here
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           redirect('donation:success', donation_amount)),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('donation:cancel')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict, button_type="donate")
    return render(request, 'base/donate.html', locals())


def successMsg(request, args):
    amount = args
    return render(request, 'base/success.html', {'amount': amount})


def cancel(request):
    return render(request, 'base/cancel.html')
