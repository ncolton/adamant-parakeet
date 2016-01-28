from django.views import generic
from django.shortcuts import render, get_object_or_404
from .models import Browser, Partner, CheckRunResult, CheckStageResult
import django.utils.timezone
from django.db.models import Q

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
        return Partner.objects.order_by('name').all()


class PartnerDetailView(generic.DetailView):
    model = Partner
    template_name = 'pik_check/partner_detail.html'


def partner_status_view(request):
    today = django.utils.timezone.now().date()
    active_after_in_past = Q(active_after__lt=today)
    inactive_after_is_null = Q(inactive_after__isnull=True)
    inactive_after_in_future = Q(inactive_after__gt=today)
    is_active_query = active_after_in_past & (inactive_after_in_future | inactive_after_is_null)
    partners = Partner.objects.filter(is_active_query).order_by('name')
    return render(request, 'pik_check/partner_status_index.html', {'partner_list': partners})


def partner_status_detail_view(request, partner_pk):
    partner = get_object_or_404(Partner, pk=partner_pk)
    check_results = {}
    for browser in partner.browsers.all():
        check_results[browser] = CheckRunResult.objects.filter(
            partner=partner).filter(browser=browser).order_by('-start_time')[:10]

    return render(
        request,
        'pik_check/partner_status_detail.html',
        {
            'partner': partner,
            'check_results': check_results
        }
    )


def check_result_detail_view(request, check_run_result_pk):
    run = get_object_or_404(CheckRunResult, pk=check_run_result_pk)
    stage_results = CheckStageResult.objects.filter(run=run).order_by('stage__ordering')
    return render(request, 'pik_check/check_result_detail.html', {'run': run, 'results': stage_results})
