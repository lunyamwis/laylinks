from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic

from django.views import View

from evangelism.models import Evangelism, Member, Minister, Ministry
from users.models import User

from .forms import (
    MemberRegistrationForm, MinisterRegistrationForm,
    MinistryRegistrationForm, EvangelismForm
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
