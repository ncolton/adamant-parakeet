from django.conf.urls import url

from . import views

app_name = 'pik_check'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^partners$', views.PartnerIndexView.as_view(), name='partner_index'),
    url(r'^partner/(?P<pk>[0-9]+)/$', views.PartnerDetailView.as_view(), name='partner_detail'),
    url(r'^browsers$', views.BrowserIndexView.as_view(), name='browser_index'),
    url(r'^browser/(?P<pk>[0-9]+)/$', views.BrowserDetailView.as_view(), name='browser_detail'),
    url(r'^job_configurations$', views.JobConfigurationIndexView.as_view(), name='job_configuration_index'),
    url(r'^job_configuration/(?P<pk>[0-9]+)/$',
        views.JobConfigurationDetailView.as_view(),
        name='job_configuration_detail')
]