from django.views import generic

from .models import JobConfiguration


class IndexView(generic.ListView):
    template_name = 'job_configuration/index.html'
    context_object_name = 'job_configuration_list'

    def get_queryset(self):
        # return JobConfiguration.objects.exclude(enabled=False)
        return JobConfiguration.objects.all()


class DetailView(generic.DetailView):
    model = JobConfiguration
    template_name = 'job_configuration/detail.html'
    context_object_name = 'job_configuration'
