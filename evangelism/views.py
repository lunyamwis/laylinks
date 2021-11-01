from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from evangelism.models import Member
from users.models import User

from .forms import (
    MemberRegistrationForm, MinisterRegistrationForm,
    MinistryRegistrationForm,EvangelismForm
)

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
            return HttpResponseRedirect('/success/')

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
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})


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
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})


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
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})

"""
class based views representations 
of the namespaces below
"""
member_registration = MemberRegistration.as_view()
minister_registration = MinisterRegistration.as_view()
ministry_registration = MinistryRegistration.as_view()
field_registration = FieldRegistration.as_view()