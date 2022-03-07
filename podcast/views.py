from django.core import serializers
from django.http import HttpResponse
from django.utils import timezone
from django.views import generic
from django.views.generic import DetailView, ListView

from . import models


class ChannelList(generic.TemplateView):
    def render_to_response(self, context, **kwargs):
        resp = self.get_data()
        return HttpResponse(resp, content_type="application/json", **kwargs)

    def get_data(self):
        qs = models.Channel.objects.all()
        return serializers.serialize("json", qs)


class ChannelDetail(generic.TemplateView):
    def render_to_response(self, context, **kwargs):
        resp = self.get_data()
        return HttpResponse(resp, content_type="application/json", **kwargs)

    def get_data(self):
        qs = models.Channel.objects.filter(slug=self.kwargs["slug"])
        return serializers.serialize("json", qs)


class ItemDetail(generic.TemplateView):
    def render_to_response(self, context, **kwargs):
        resp = self.get_data()
        return HttpResponse(resp, content_type="application/json", **kwargs)

    def get_data(self):
        qs = models.Item.objects.filter(slug=self.kwargs["item"])
        return serializers.serialize("json", qs)


class Channels(ListView):
    model = models.Channel
    template_name = "podcast/list.html"
    paginate_by = 10  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class Item(DetailView):
    model = models.Item
    template_name = "podcast/detail.html"


class RSSFeed(generic.TemplateView):
    template_name = "podcast/rss_feed.html"
    content_type = "application/rss+xml"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["channel"] = models.Channel.objects.prefetch_related("item_set").get(
            slug=self.kwargs["channel"]
        )

        return context
