from django.shortcuts import redirect, render
from django.views.generic import View

from donation.forms import DonationForm
from payment.models import Payment


def index(request):
    return render(request, "base/index.html")


class DonationView(View):
    def get(self, request):
        f = DonationForm()
        return render(request, "base/subscription_form.html", context={"f": f})

    def post(self, request):
        """This view is for donations"""
        payment = Payment()
        payment.payment_purpose = "D"
        if request.method == "POST":
            f = DonationForm(request.POST)
            if f.is_valid():
                amount = request.POST.get("amount")
                request.session["amount"] = amount
                payment.total = int(amount)
                payment.save()
                return redirect("core:checkout")
        else:
            f = DonationForm()
        return render(request, "base/subscription_form.html", locals())


def successMsg(request, args):
    amount = args
    return render(request, "base/success.html", {"amount": amount})


def cancel(request):
    return render(request, "base/cancel.html")
