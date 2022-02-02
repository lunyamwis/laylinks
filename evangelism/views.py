"""
Date: 01/02/2022
Author: Martin Luther Bironga
Purpose: Evangelism Registrations and Workflows
"""

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.forms.models import construct_instance
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic.list import ListView
from formtools.wizard.views import SessionWizardView

from evangelism.models import Evangelism, Member, Minister, Ministry

from .forms import (
    ChurchMemberDetailsForm,
    ChurchMinisterDetailsForm,
    ContactMinisterDetailsForm,
    EvangelismForm,
    EventDetails,
    Logistics,
    MemberRegistrationForm,
    MinistryRegistrationForm,
    SermonDetails,
    SurveyForm,
)

FORMS = [
    ("member_details", MemberRegistrationForm),
    ("church_details", ChurchMemberDetailsForm),
]

MINISTER_FORMS = [
    ("minister_details", MinistryRegistrationForm),
    ("church_details", ChurchMinisterDetailsForm),
    ("contact_details", ContactMinisterDetailsForm),
]

MINISTRY_FORMS = [("ministry_details", MinistryRegistrationForm)]

EVANGELISM_FORMS = [
    ("field_details", EvangelismForm),
    ("event_details", EventDetails),
    ("sermon_details", SermonDetails),
    ("logistic_details", Logistics),
    ("survey_details", SurveyForm),
]


class MemberRegistrationWizzard(SessionWizardView):
    """this class is for registering a member"""

    form_list = FORMS
    template_name = "evangelism/wizzard.html"

    def done(self, form_list, form_dict):
        """
        stepwise form for registering a member to the members database table
        step 1: save the member details
        step 2: save the church details
        """
        instance = Member()
        for form in form_list:
            instance = construct_instance(
                form, instance, form._meta.fields, form._meta.exclude
            )

            # check whether the passwords match if they do, then we can hash them
            if instance.password == instance.password2:
                instance.password = make_password(instance.password)
                instance.password2 = make_password(instance.password2)
            else:
                form_dict["member_details"].errors[
                    "password"
                ] = "Passwords do not match"

        # save the instance to the Members table
        instance.save()

        # send a confirmation email to the user who has just signed in
        send_mail(
            subject="Confirmation Email",
            message="Please click the link below in order to activate your account\n"
            + f"{self.request.get_host()}?confirm_email={True}&member={instance.pk}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
            fail_silently=False,
        )

        # send a message to assure the individual has successfully signed in
        messages.success(
            self.request,
            message="You have successfully registered as a member of laylinks,\n"
            + "we have sent you a confirmation email please confirm in order to"
            + " activate your account",
        )

        return redirect("/")


class MemberListView(ListView):
    """this class is meant to enlist the members"""

    model = Member
    paginate_by = 15
    template_name = "evangelism/list.html"

    def get_context_data(self, **kwargs):
        """this function helps assign variables to the jinja templates"""
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        context["data"] = "member"
        return context


class MinisterRegistrationWizzard(SessionWizardView):
    """this class is for registering a minister"""

    form_list = MINISTER_FORMS
    template_name = "evangelism/wizzard.html"

    def done(self, form_list, form_dict):
        """
        stepwise form for registering a minister to the ministers database table
        step 1: save the minister details
        step 2: save the church details
        """
        instance = Minister()
        for form in form_list:
            instance = construct_instance(
                form, instance, form._meta.fields, form._meta.exclude
            )

            # check whether the passwords match if they do, then we can hash them
            if instance.password == instance.password2:
                instance.password = make_password(instance.password)
                instance.password2 = make_password(instance.password2)
            else:
                form_dict["minister_details"].errors[
                    "password"
                ] = "Passwords do not match"

        # save the instance to the Members table
        instance.save()

        # send a confirmation email to the user who has just signed in
        send_mail(
            subject="Confirmation Email",
            message="Please click the link below in order to activate your account\n"
            + f"{self.request.get_host()}?confirm_email={True}&minister={instance.pk}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
            fail_silently=False,
        )

        # send a message to assure the individual has successfully signed in
        messages.success(
            self.request,
            message="You have successfully registered as a minister in laylinks,\n"
            + "we have sent you a confirmation email"
            + " please confirm in order to activate your account",
        )
        return redirect("/")


class MinisterListView(ListView):
    """this class is meant to enlist the ministers"""

    model = Minister
    paginate_by = 15
    template_name = "evangelism/list.html"

    def get_context_data(self, **kwargs):
        """this function helps assign variables to the jinja templates"""
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        context["data"] = "minister"
        return context


class MinistryRegistrationWizzard(SessionWizardView):
    """this class is for registering a ministry"""

    form_list = MINISTRY_FORMS
    template_name = "evangelism/wizzard.html"

    def done(self, form_list, form_dict):
        """
        stepwise form for registering a minister to the ministers database table
        step 1: save the minister details
        step 2: save the church details
        """
        instance = Ministry()
        for form in form_list:
            instance = construct_instance(
                form, instance, form._meta.fields, form._meta.exclude
            )

            # check whether the passwords match if they do, then we can hash them
            if instance.password == instance.password2:
                instance.password = make_password(instance.password)
                instance.password2 = make_password(instance.password2)
            else:
                form_dict["ministry_details"].errors[
                    "password"
                ] = "Passwords do not match"

        # save the instance to the Members table
        instance.save()

        # send a confirmation email to the user who has just signed in
        send_mail(
            subject="Confirmation Email",
            message="Please click the link below in order to activate your account\n"
            + f"{self.request.get_host()}?confirm_email={True}&ministry={instance.pk}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
            fail_silently=False,
        )

        # send a message to assure the individual has successfully signed in
        messages.success(
            self.request,
            message="You have successfully registered as a ministry in laylinks,\n"
            + "we have sent you a confirmation email "
            + "please confirm in order to activate your account",
        )
        return redirect("/")


class MinistryListView(ListView):
    """this class is meant to enlist the ministries"""

    model = Ministry
    paginate_by = 15
    template_name = "evangelism/list.html"

    def get_context_data(self, **kwargs):
        """this function helps assign variables to the jinja templates"""
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        context["data"] = "ministry"
        return context


class EvangelismWizzard(SessionWizardView):
    """this class is for taking a member through inviting a minister or ministry"""

    def done(self):
        """this functions manipulates the invitation form"""
        return redirect("/")


def field_detail(request, **kwargs):
    """this function gives us another approach of manipulating the invitation form"""
    name = kwargs["name"]
    if Minister.objects.filter(name=name).exists():
        minister_ry = Minister.objects.get(name=name)
    else:
        minister_ry = Ministry.objects.get(name=name)
    form = EvangelismForm(request.POST or None)
    if form.is_valid():
        form.save()
        field = Evangelism.objects.get(id=form.instance.pk)
        minister_ry.fields.add(field)
    return render(request, "evangelism/form.html", {"form": form})
