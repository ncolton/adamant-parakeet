from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Partner, Browser, JobConfiguration


def create_browser(browser_name):
    return Browser.objects.create(name=browser_name)


def create_partner(partner_code, partner_name):
    return Partner.objects.create(code=partner_code, name=partner_name)


def create_job_configuration(partner, scheduling_interval, enabled):
    return JobConfiguration.objects.create(
        partner=partner,
        scheduling_interval=scheduling_interval,
        enabled=enabled
    )


class JobConfigurationModelTests(TestCase):
    def test_adding_browsers(self):
        p = create_partner(partner_code='Job', partner_name='Job Partner')
        b = create_browser(browser_name='Job Browser')
        j = JobConfiguration(partner=p, enabled=True, scheduling_interval=2)
        j.save()
        j.browsers.add(b)
        j.save()

        self.assertEqual(j.browsers.count(), 1)


class PartnerViewTests(TestCase):
    def test_index_view_with_no_partners(self):
        response = self.client.get(reverse('pik_check:partner_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No partners are available.")
        self.assertQuerysetEqual(response.context['partner_list'], [])

    def test_index_view_with_a_partner(self):
        expected_partner = create_partner('foo', 'Foo Industries')
        response = self.client.get(reverse('pik_check:partner_index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['partner_list'], [repr(expected_partner)])


class PartnerDetailViewTests(TestCase):
    def test_detail_view_with_a_partner(self):
        partner = create_partner(partner_code='detpart', partner_name='Detailed Partner')
        response = self.client.get(reverse('pik_check:partner_detail', args=(partner.id,)))
        self.assertContains(response, partner.name, status_code=200)


class JobConfigurationViewTests(TestCase):
    def test_index_view_with_no_job_configurations(self):
        response = self.client.get(reverse('pik_check:job_configuration_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No job configurations are available.")
        self.assertQuerysetEqual(response.context['job_configuration_list'], [])

    def test_index_view_with_a_job_configuration(self):
        p = create_partner(partner_code='Job', partner_name='Job Partner')
        b = create_browser(browser_name='Job Browser')
        j = create_job_configuration(partner=p, scheduling_interval=2, enabled=True)
        j.browsers.add(b)
        j.save()

        response = self.client.get(reverse('pik_check:job_configuration_index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['job_configuration_list'], [repr(j)])


class PartnerDetailViewTests(TestCase):
    def test_detail_view_with_a_job_configuration(self):
        # partner = create_partner(partner_code='detpart', partner_name='Detailed Partner')
        # response = self.client.get(reverse('job_configuration:detail', args=(partner.id,)))
        # self.assertContains(response, partner.name, status_code=200)
        pass


class BrowserMethodTests(TestCase):
    def test_unicode_output(self):
        self.assertEqual(str(create_browser(u'Potato')), 'Potato')


class BrowserViewTests(TestCase):
    def test_index_view_with_no_browsers(self):
        response = self.client.get(reverse('pik_check:browser_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No browsers are available.")
        self.assertQuerysetEqual(response.context['browser_list'], [])

    def test_index_view_with_a_browser(self):
        expected_browser = create_browser('Foo Browser')
        response = self.client.get(reverse('pik_check:browser_index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['browser_list'], [repr(expected_browser)])


class BrowserDetailViewTests(TestCase):
    def test_detail_view_with_a_browser(self):
        browser = create_browser(browser_name='Detailed Browser')
        response = self.client.get(reverse('pik_check:browser_detail', args=(browser.id,)))
        self.assertContains(response, browser.name, status_code=200)
