from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, render
from django.views import generic


from django.views import View
from django.forms.models import construct_instance
from evangelism.models import Evangelism, Member, Minister, Ministry
from users.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate
from formtools.wizard.views import (
    SessionWizardView,
    NamedUrlWizardView
)

from .forms import (
    MemberRegistrationForm, ChurchMemberDetailsForm, MinisterRegistrationForm,
    ChurchMinisterDetailsForm, ContactMinisterDetailsForm,
    MinistryRegistrationForm, EvangelismForm, EventDetails,
    SermonDetails, Logistics, SurveyForm
)
FORMS = [("member_details", MemberRegistrationForm),
         ("church_details", ChurchMemberDetailsForm)]

MINISTRY_FORMS = [("minister_details", MinistryRegistrationForm),
                  ("church_details", ChurchMinisterDetailsForm),
                  ("contact_details", ContactMinisterDetailsForm)]

EVANGELISM_FORMS = [("field_details", EvangelismForm),
                    ("event_details", EventDetails),
                    ("sermon_details", SermonDetails),
                    ("logistic_details", Logistics),
                    ("survey_details", SurveyForm)]

TEMPLATES = {"member_details": "evangelism/wizzard.html",
             "church_details": "evangelism/wizzard.html", }

MINISTRY_TEMPLATES = {"minister_details": "evangelism/wizzard.html",
                      "church_details": "evangelism/wizzard.html",
                      "contact_details": "evangelism/wizzard.html", }

EVANGELISM_TEMPLATES = {"field_details": "evangelism/wizzard.html",
                        "event_details": "evangelism/wizzard.html",
                        "sermon_details": "evangelism/wizzard.html",
                        "logistic_details": "evangelism/wizzard.html",
                        "survey_details": "evangelism/wizzard.html"}


class MemberRegistrationWizzard(SessionWizardView):

    form_list = FORMS
    template_name = "evangelism/wizzard.html"

    def done(self, form_list, form_dict, ** kwargs):
        """
        stepwise form for registering a member to the members database table
        step 1: save the member details
        step 2: save the church details
        """
        instance = Member()
        for form in form_list:
            instance = construct_instance(
                form, instance, form._meta.fields, form._meta.exclude)

            # check whether the passwords match if they do, then we can hash them
            if instance.password == instance.password2:
                instance.password = make_password(instance.password)
                instance.password2 = make_password(instance.password2)
            else:
                form_dict['member_details'].errors['password'] = "Passwords do not match"

        # save the instance to the Members table
        instance.save()

        # also we open a members account too once is completed registering
        user = User()
        user.username = instance.name
        user.email = instance.email
        user.password = instance.password
        user.is_member = True
        user.save()
        return redirect('/')


class MinisterRegistrationWizzard(SessionWizardView):

    def get_template_names(self):
        return [MINISTRY_TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        return redirect('/')


class EvangelismWizzard(SessionWizardView):

    def get_template_names(self):
        return [EVANGELISM_TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        return redirect('/')


class MemberRegistration(View):
    form_class = MemberRegistrationForm
    initial = {'key': 'value'}
    template_name = 'evangelism/form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            user = User()
            user.username = form.instance.name
            user.email = form.instance.email
            user.password = form.instance.password
            user.is_member = True
            user.save()
            return HttpResponseRedirect('/')

        return render(request, self.template_name, {'form': form})


class MinisterRegistration(View):
    form_class = MinisterRegistrationForm
    initial = {'key': 'value'}
    template_name = 'evangelism/form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            user = User()
            user.username = form.instance.name
            user.email = form.instance.email
            user.password = form.instance.password
            user.is_minister = True
            user.save()
            return HttpResponseRedirect('/')

        return render(request, self.template_name, {'form': form})


class MinisterListView(generic.ListView):
    template_name = "evangelism/list.html"
    queryset = Minister.objects.all()

    def get_context_data(self, **kwargs):
        context = {}
        context['data'] = 'minister'
        context['object_list'] = self.queryset
        return context


class MinisterDetailView(generic.DetailView):
    template_name = "evangelism/detail.html"
    queryset = Minister.objects.all()


class MinistryRegistration(View):
    form_class = MinistryRegistrationForm
    initial = {'key': 'value'}
    template_name = 'evangelism/form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            user = User()
            user.username = form.instance.name
            user.email = form.instance.email
            user.password = form.instance.password
            user.is_ministry = True
            user.save()
            return HttpResponseRedirect('/')

        return render(request, self.template_name, {'form': form})


class MinistryListView(generic.ListView):
    template_name = "evangelism/list.html"
    queryset = Ministry.objects.all()

    def get_context_data(self, **kwargs):
        context = {}
        context['data'] = 'ministry'
        context['object_list'] = self.queryset
        return context


class MinistryDetailView(generic.DetailView):
    template_name = "evangelism/detail.html"
    queryset = Ministry.objects.all()


class FieldRegistration(View):
    form_class = EvangelismForm
    initial = {'key': 'value'}
    template_name = 'evangelism/form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')

        return render(request, self.template_name, {'form': form})


class FieldListView(generic.ListView):
    template_name = "evangelism/list.html"
    queryset = Evangelism.objects.all()

    def get_context_data(self, **kwargs):
        context = {}
        context['data'] = 'field'
        context['object_list'] = self.queryset
        return context


def field_detail(request, *args, **kwargs):
    name = kwargs['name']
    if Minister.objects.filter(
            name=name).exists():
        minister_ry = Minister.objects.get(
            name=name)
    else:
        minister_ry = Ministry.objects.get(name=name)
    form = EvangelismForm(request.POST or None)
    if form.is_valid():
        form.save()
        field = Evangelism.objects.get(id=form.instance.pk)
        minister_ry.fields.add(field)
    return render(request, "evangelism/form.html", {
        "form": form
    })


"""
class based views representations of the namespaces below
"""
member_registration = MemberRegistration.as_view()
minister_registration = MinisterRegistration.as_view()
ministry_registration = MinistryRegistration.as_view()
field_registration = FieldRegistration.as_view()
