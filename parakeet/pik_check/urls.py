from django.conf.urls import url

from . import views

app_name = 'pik_check'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^partners$', views.PartnerIndexView.as_view(), name='partner_index'),
    # url(r'^partner/(?P<pk>[0-9]+)/$', views.PartnerDetailView.as_view(), name='partner_detail'),
    url(r'^partner/(?P<pk>[0-9]+)/$', views.partner_detail_view, name='partner_detail'),
    url(r'^status/partners$', views.partner_status_view, name='partner_status_index'),
    url(r'^status/partner/(?P<partner_pk>[0-9]+)/$',
        views.partner_status_detail_view,
        name='partner_status_detail'),
    url(r'^status/check_run_result/(?P<check_run_result_pk>[0-9]+)/$',
        views.check_result_detail_view,
        name='check_result_detail'),
    url(r'^browsers$', views.BrowserIndexView.as_view(), name='browser_index'),
    url(r'^browser/(?P<pk>[0-9]+)/$', views.BrowserDetailView.as_view(), name='browser_detail')
]
