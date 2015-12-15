from django.views import generic

from .models import Browser


class IndexView(generic.ListView):
    template_name = 'browsers/index.html'
    context_object_name = 'browser_list'

    def get_queryset(self):
        return Browser.objects.all()


class DetailView(generic.DetailView):
    model = Browser
    template_name = 'browsers/detail.html'
