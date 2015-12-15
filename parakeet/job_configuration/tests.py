from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import JobConfiguration
from partners.models import Partner
from browsers.models import Browser


class JobConfigurationViewTests(TestCase):
    def test_index_view_with_no_job_configurations(self):
        response = self.client.get(reverse('job_configuration:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No job configurations are available.")
        self.assertQuerysetEqual(response.context['job_configuration_list'], [])

    def test_index_view_with_a_job_configuration(self):
        # partner =
        # expected_job_configuration = create_job_configuration()
        p = Partner(code='Job', name='Job Partner')
        b = Browser(name='Job Browser')
        j = JobConfiguration(partner=p, enabled=True)

        # response = self.client.get(reverse('job_configuration:index'))
        # self.assertEqual(response.status_code, 200)
        # self.assertQuerysetEqual(response.context['job_configuration_list'], [repr(expected_partner)])


class PartnerDetailViewTests(TestCase):
    def test_detail_view_with_a_job_configuration(self):
        # partner = create_partner(partner_code='detpart', partner_name='Detailed Partner')
        # response = self.client.get(reverse('job_configuration:detail', args=(partner.id,)))
        # self.assertContains(response, partner.name, status_code=200)
        pass
