"""
Date: 01/02/2022
Author: Martin Luther Bironga
Purpose: Evangelism Registrations and Workflows
"""
from collections import OrderedDict

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.forms.models import construct_instance
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic.detail import DetailView
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
        context["data"] = "members"
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


class MinisterDetailView(DetailView):
    model = Minister
    template_name = "evangelism/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

    form_list = EVANGELISM_FORMS
    template_name = "evangelism/wizzard.html"

    def get_form_list(self):

        form_list = OrderedDict()

        cleaned_data = self.get_cleaned_data_for_step("field_details") or {}

        for form_key, form_class in self.form_list.items():
            if cleaned_data and cleaned_data["is_event"] == "S":
                if form_key == "event_details":
                    continue
                else:
                    pass

            # try to fetch the value from condition list, by default, the form
            # gets passed to the new list.
            condition = self.condition_dict.get(form_key, True)
            if callable(condition):
                # call the value if needed, passes the current instance.
                condition = condition(self)
            if condition:
                form_list[form_key] = form_class
        return form_list

    def done(self, form_list, form_dict):
        """
        step 1 - if member fills in the event to be sermon details it should
        take them direct to filling in sermon details and if they fill it in as
        an event then it should directly take them to event details
        step 2 - if an event/invitation is completed then it should mark of the
        is_completed flag to true, and report that the form has been completed to 100%
        step 3 - an email should be sent to the ministers / ministries upon completion
        of the form.
        """
        instance = Evangelism()
        for form in form_list:
            instance = construct_instance(
                form, instance, form._meta.fields, form._meta.exclude
            )

        instance.save()

        # assign an event to a minister
        minister_pk = self.request.GET.get("minister")
        ministry_pk = self.request.GET.get("ministry")
        if minister_pk:
            minister = Minister.objects.get(pk=minister_pk)
            minister.fields.add(instance)
            # notify the minister that you have invited them for an event
            send_mail(
                subject="Invitation Email",
                message=f"Hey {minister.name},\n"
                + "you have been invited to the following event\n"
                + f"{self.request.get_host()}/evangelism/field/list/",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[minister.email],
                fail_silently=False,
            )
            send_mail(
                subject="Invitation Email",
                message=f"Hey {minister.contact_assistant_name},\n"
                + f"Minister {minister.name} has been invited to the following event\n"
                + f"{self.request.get_host()}/evangelism/field/list/",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[minister.contact_assistant_email],
                fail_silently=False,
            )
        elif ministry_pk:
            ministry = Ministry.objects.get(pk=ministry_pk)
            ministry.fields.add(instance)
            # notify the minister that you have invited them for an event
            send_mail(
                subject="Invitation Email",
                message=f"Hey {ministry.name},\n"
                + "you have been invited to the following event\n"
                + f"{self.request.get_host()}/evangelism/field/list/",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[ministry.email],
                fail_silently=False,
            )

        messages.success(
            request=self.request,
            message="Successfully sent an invitation, "
            + "please wait for a confirmation notice",
        )

        return redirect("/")


class EvangelismListView(ListView):
    """this class is meant to enlist the ministries"""

    model = Evangelism
    paginate_by = 15
    template_name = "evangelism/list.html"

    def get_context_data(self, **kwargs):
        """this function helps assign variables to the jinja templates"""
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        context["data"] = "field"
        return context


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
