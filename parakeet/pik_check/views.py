from django.views import generic
from django.shortcuts import render

from .models import Browser, JobConfiguration, Partner


def index(request):
    return render(request, 'pik_check/index.html')


class BrowserIndexView(generic.ListView):
    template_name = 'pik_check/browser_index.html'
    context_object_name = 'browser_list'

    def get_queryset(self):
        return Browser.objects.all()


class BrowserDetailView(generic.DetailView):
    model = Browser
    template_name = 'pik_check/browser_detail.html'


class PartnerIndexView(generic.ListView):
    template_name = 'pik_check/partner_index.html'
    context_object_name = 'partner_list'

    def get_queryset(self):
        return Partner.objects.all()


class PartnerDetailView(generic.DetailView):
    model = Partner
    template_name = 'pik_check/partner_detail.html'


class JobConfigurationIndexView(generic.ListView):
    template_name = 'pik_check/job_configuration_index.html'
    context_object_name = 'job_configuration_list'

    def get_queryset(self):
        # return JobConfiguration.objects.exclude(enabled=False)
        return JobConfiguration.objects.all()


class JobConfigurationDetailView(generic.DetailView):
    model = JobConfiguration
    template_name = 'pik_check/job_configuration_detail.html'
    context_object_name = 'job_configuration'
