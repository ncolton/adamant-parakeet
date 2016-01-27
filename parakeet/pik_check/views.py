from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import render, get_object_or_404

from .models import Browser, JobConfiguration, Partner, CheckRunResult, CheckStageResult
from .forms import NewJobConfigurationForm, JobConfigurationForm


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


class JobConfigurationFormView(generic.FormView):
    template_name = 'pik_check/job_configuration_form.html'
    form_class = NewJobConfigurationForm

    def form_valid(self, form):
        j = JobConfiguration(
            partner=form.cleaned_data['partner'],
            enabled=form.cleaned_data['enabled'],
            scheduling_interval=form.cleaned_data['scheduling_interval']
        )
        j.save()
        for browser in form.cleaned_data['browsers']:
            j.browsers.add(browser)
        j.save()

        return HttpResponseRedirect(reverse('pik_check:job_configuration_detail', kwargs={'pk': j.id}))


def partner_status_view(request):
    partners = Partner.objects.filter(jobconfiguration__isnull=False).order_by('name')
    return render(request, 'pik_check/partner_status_index.html', {'partner_list': partners})


def partner_status_detail_view(request, partner_pk):
    partner = get_object_or_404(Partner, pk=partner_pk)
    job_config = JobConfiguration.objects.filter(partner=partner).first()
    check_results = {}
    if job_config:
        for browser in job_config.browsers.all():
            check_results[browser] = CheckRunResult.objects.filter(
                partner=partner).filter(browser=browser).order_by('-start_time')[:10]

    return render(
        request,
        'pik_check/partner_status_detail.html',
        {
            'partner': partner,
            'job_config': job_config,
            'check_results': check_results
        }
    )


def check_result_detail_view(request, check_run_result_pk):
    run = get_object_or_404(CheckRunResult, pk=check_run_result_pk)
    stage_results = CheckStageResult.objects.filter(run=run).order_by('stage__ordering')
    return render(request, 'pik_check/check_result_detail.html', {'run': run, 'results': stage_results})


def partner_job_edit_view(request, partner_id=None):
    partner = get_object_or_404(Partner, id=partner_id)
    try:
        job_configuration = JobConfiguration.objects.get(partner=partner)
    except JobConfiguration.DoesNotExist:
        job_configuration = JobConfiguration(partner=partner)

    form = JobConfigurationForm(request.POST or None, instance=job_configuration)

    if request.POST:
        if form.is_valid():
            job_configuration = form.save()
            redirect_url = reverse('pik_check:job_configuration_detail', kwargs={'pk': job_configuration.id})
            return HttpResponseRedirect(redirect_url)
    return render(request, 'pik_check/partner_edit_job.html', {'form': form, 'partner': partner})
