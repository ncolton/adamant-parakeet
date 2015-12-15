from django.shortcuts import get_object_or_404, render
from django.template import RequestContext, loader
from django.views import generic

from .models import Partner


class IndexView(generic.ListView):
    template_name = 'partners/index.html'
    context_object_name = 'partner_list'

    def get_queryset(self):
        return Partner.objects.all()


class DetailView(generic.DetailView):
    model = Partner
    template_name = 'partners/detail.html'
