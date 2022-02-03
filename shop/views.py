import random
import string

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse
from django.utils import timezone
from django.views.generic import DetailView, ListView, View

# Payment
from payment.models import Payment

from .forms import CheckoutForm, CouponForm, PaymentForm, RefundForm
from .models import Address, Coupon, Item, Order, OrderItem, Refund, UserProfile

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_ref_code():
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=20))


def products(request):
    context = {"items": Item.objects.all()}
    return render(request, "products.html", context)


def is_valid_form(values):
    valid = True
    for field in values:
        if field == "":
            valid = False
    return valid


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                "form": form,
                "couponform": CouponForm(),
                "order": order,
                "DISPLAY_COUPON_FORM": True,
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user, address_type="S", default=True
            )
            if shipping_address_qs.exists():
                context.update({"default_shipping_address": shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user, address_type="B", default=True
            )
            if billing_address_qs.exists():
                context.update({"default_billing_address": billing_address_qs[0]})
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get("use_default_shipping")
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user, address_type="S", default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available"
                        )
                        return redirect("core:checkout")
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get("shipping_address")
                    shipping_address2 = form.cleaned_data.get("shipping_address2")
                    shipping_country = form.cleaned_data.get("shipping_country")
                    shipping_zip = form.cleaned_data.get("shipping_zip")

                    if is_valid_form(
                        [shipping_address1, shipping_country, shipping_zip]
                    ):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type="S",
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            "set_default_shipping"
                        )
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request,
                            "Please fill in the required shipping address fields",
                        )

                use_default_billing = form.cleaned_data.get("use_default_billing")
                same_billing_address = form.cleaned_data.get("same_billing_address")

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = "B"
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user, address_type="B", default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available"
                        )
                        return redirect("core:checkout")
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get("billing_address")
                    billing_address2 = form.cleaned_data.get("billing_address2")
                    billing_country = form.cleaned_data.get("billing_country")
                    billing_zip = form.cleaned_data.get("billing_zip")

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type="B",
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            "set_default_billing"
                        )
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request,
                            "Please fill in the required billing address fields",
                        )

                payment_option = form.cleaned_data.get("payment_option")

                if payment_option == "S":
                    return redirect("core:payment", payment_option="stripe")
                elif payment_option == "Paypal":
                    return redirect("core:payment", payment_option="paypal")
                else:
                    messages.warning(self.request, "Invalid payment option selected")
                    return redirect("core:checkout")
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:order-summary")


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        host = self.request.get_host()
        amount = int(order.get_total())
        if order.billing_address or order.shipping_address:

            payment = Payment()
            payment.variant = "Paypal"
            payment.user = self.request.user
            payment.total = order.get_total()
            payment.tax = order.get_total() * 0.1
            payment.delivery = order.get_total() * 0.05

            # import pdb
            # pdb.set_trace()
            if order.billing_address:
                billing_address = order.billing_address
                payment.billing_first_name = billing_address.user.first_name
                payment.billing_last_name = billing_address.user.last_name
                payment.billing_address_1 = billing_address.street_address
                payment.billing_address_2 = billing_address.apartment_address
                payment.billing_country_area = billing_address.country
                payment.billing_country_code = billing_address.country

            elif order.shipping_address:
                shipping_address = order.shipping_address
                payment.billing_first_name = shipping_address.user.first_name
                payment.billing_last_name = shipping_address.user.last_name
                payment.billing_address_1 = shipping_address.street_address
                payment.billing_address_2 = shipping_address.apartment_address
                payment.billing_country_area = shipping_address.country
                payment.billing_country_code = shipping_address.country

            payment.save()

            # assign the payment to the order

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            order.ref_code = create_ref_code()
            order.save()

            messages.success(self.request, "Your order was successful!")
            return redirect("payment:payment_details", payment_id=payment.id)
        else:
            messages.warning(self.request, "You have not added a billing address")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        host = self.request.get_host()
        userprofile = UserProfile.objects.get(user=self.request.user)
        # import pdb
        # pdb.set_trace()
        if form.is_valid():
            save = form.cleaned_data.get("save")
            use_default = form.cleaned_data.get("use_default")

            if save:

                userprofile.one_click_purchasing = True
                userprofile.save()

            amount = int(order.get_total())

            try:

                if order.billing_address or order.shipping_address:

                    payment = Payment()
                    payment.variant = form.cleaned_data.get("payment_option")

                    payment.user = self.request.user
                    payment.total = order.get_total()
                    payment.tax = order.get_total() * 0.1
                    payment.delivery = order.get_total() * 0.05

                    # import pdb
                    # pdb.set_trace()
                    billing_address = order.billing_address
                    payment.billing_first_name = billing_address.user.first_name
                    payment.billing_last_name = billing_address.user.last_name
                    payment.billing_address_1 = billing_address.street_address
                    payment.billing_address_2 = billing_address.apartment_address
                    payment.billing_country_area = billing_address.country
                    payment.billing_country_code = billing_address.country

                    if order.shipping_address:
                        shipping_address = order.shipping_address
                        payment.billing_first_name = shipping_address.user.first_name
                        payment.billing_last_name = shipping_address.user.last_name
                        payment.billing_address_1 = shipping_address.street_address
                        payment.billing_address_2 = shipping_address.apartment_address
                        payment.billing_country_area = shipping_address.country
                        payment.billing_country_code = shipping_address.country

                    payment.payment_purpose = "B"
                    payment.save()

                    # assign the payment to the order

                    order_items = order.items.all()
                    order_items.update(ordered=True)
                    for item in order_items:
                        item.save()

                    order.ordered = True
                    order.payment = payment
                    order.ref_code = create_ref_code()
                    order.save()

            except Exception as e:
                # send an email to ourselves
                messages.warning(
                    self.request, "A serious error occurred. We have been notifed."
                )
                return redirect("/")

        messages.success(self.request, "Your order was successful!")
        return redirect("payment:payment_details", payment_id=payment.id)


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {"object": order}
            return render(self.request, "order_summary.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get("code")
                order = Order.objects.get(user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {"form": form}
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get("ref_code")
            message = form.cleaned_data.get("message")
            email = form.cleaned_data.get("email")
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("core:request-refund")
