from __future__ import absolute_import
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.core.urlresolvers import reverse
from pik_check import models
import datetime
import django.utils.timezone
from . import factories


class PartnerModelTests(TestCase):
    def test_no_start_date_means_not_enabled(self):
        partner = factories.PartnerFactory()
        self.assertEqual(partner.active_after, None)
        self.assertFalse(partner.is_active)

    def test_start_date_in_future_means_not_enabled(self):
        partner = factories.PartnerFactory()
        partner.active_after = django.utils.timezone.now().date() + datetime.timedelta(days=1)
        partner.save()
        self.assertFalse(partner.is_active)

    def test_start_date_in_past_means_enabled(self):
        partner = factories.PartnerFactory()
        partner.active_after = django.utils.timezone.now().date() - datetime.timedelta(days=1)
        partner.save()
        self.assertTrue(partner.is_active)

    def test_end_date_in_future_means_enabled(self):
        partner = factories.PartnerFactory()
        partner.active_after = django.utils.timezone.now().date() - datetime.timedelta(days=100)
        partner.inactive_after = django.utils.timezone.now().date() + datetime.timedelta(days=1)
        partner.save()
        self.assertTrue(partner.is_active)

    def test_end_date_in_past_means_disabled(self):
        partner = factories.PartnerFactory()
        partner.active_after = django.utils.timezone.now().date() - datetime.timedelta(days=100)
        partner.inactive_after = django.utils.timezone.now().date() - datetime.timedelta(days=1)
        partner.save()
        self.assertFalse(partner.is_active)

    def test_start_date_after_end_date_is_invalid(self):
        partner = factories.PartnerFactory()
        partner.active_after = django.utils.timezone.now().date()
        partner.inactive_after = django.utils.timezone.now().date() - datetime.timedelta(days=1)
        with self.assertRaises(ValidationError):
            partner.full_clean()

    def test_lower_case_code_is_invalid(self):
        partner = models.Partner(name='foo', code='foo')
        with self.assertRaises(ValidationError):
            partner.full_clean()

    def test_can_associate_a_browser(self):
        partner = factories.PartnerFactory()
        browser = factories.BrowserFactory()
        self.assertEqual(partner.browsers.count(), 0)
        partner.browsers.add(browser)
        self.assertEqual(partner.browsers.count(), 1)

    def test_can_associate_multiple_browsers(self):
        partner = factories.PartnerFactory()
        browser1 = factories.BrowserFactory()
        browser2 = factories.BrowserFactory()
        self.assertEqual(partner.browsers.count(), 0)
        partner.browsers.add(browser1)
        partner.browsers.add(browser2)
        self.assertEqual(partner.browsers.count(), 2)


class PartnerViewTests(TestCase):
    def test_call_view_loads(self):
        response = self.client.get(reverse('pik_check:partner_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pik_check/partner_index.html')

    def test_index_view_with_no_partners(self):
        response = self.client.get(reverse('pik_check:partner_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No partners are configured.")
        self.assertQuerysetEqual(response.context['partner_list'], [])

    def test_index_view_with_a_partner(self):
        expected_partner = factories.PartnerFactory()
        response = self.client.get(reverse('pik_check:partner_index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['partner_list'], [repr(expected_partner)])

    def test_index_view_of_partner_with_future_activation_indicates_activation_date(self):
        partner = factories.PartnerFactory()
        partner.active_after = django.utils.timezone.now().date() + datetime.timedelta(days=1)
        partner.full_clean()
        partner.save()
        response = self.client.get(reverse('pik_check:partner_index'))
        self.assertContains(response, 'Active After: ', count=1)

    def test_index_view_of_partner_with_passed_inactive_after_indicates_deactivation_date(self):
        partner = factories.PartnerFactory()
        partner.active_after = django.utils.timezone.now().date() - datetime.timedelta(days=2)
        partner.inactive_after = django.utils.timezone.now().date() - datetime.timedelta(days=1)
        partner.full_clean()
        partner.save()
        response = self.client.get(reverse('pik_check:partner_index'))
        self.assertNotContains(response, 'Active After:')
        self.assertContains(response, 'Inactive After: ', count=1)

    def test_index_view_of_partner_with_future_inactive_after_indicates_deactivation_date(self):
        partner = factories.PartnerFactory()
        partner.active_after = django.utils.timezone.now().date() - datetime.timedelta(days=1)
        partner.inactive_after = django.utils.timezone.now().date() + datetime.timedelta(days=1)
        partner.full_clean()
        partner.save()
        response = self.client.get(reverse('pik_check:partner_index'))
        self.assertTrue(partner.is_active)
        self.assertNotContains(response, 'Active After:')
        self.assertContains(response, 'Inactive After: ', count=1)


class PartnerDetailViewTests(TestCase):
    def test_call_view_loads(self):
        partner = factories.PartnerFactory()
        response = self.client.get(reverse('pik_check:partner_detail', args=[partner.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pik_check/partner_detail.html')

    def test_detail_view_with_a_partner(self):
        partner = factories.PartnerFactory()
        response = self.client.get(reverse('pik_check:partner_detail', args=(partner.id,)))
        self.assertContains(response, partner.name, status_code=200)

    def test_detail_view_of_disabled_partner_indicates_partner_is_disabled(self):
        self.skipTest('not implemented yet')
        partner = factories.PartnerFactory()
        partner.active_after = django.utils.timezone.now().date() - datetime.timedelta(days=1)
        partner.inactive_after = django.utils.timezone.now().date() - datetime.timedelta(days=1)
        partner.full_clean()
        partner.save()
        response = self.client.get(reverse('pik_check:partner_detail', args=(partner.id,)))
        self.assertFalse(partner.is_active)
        # This seems silly, and ties awfully close to the template implementation...
        self.assertContains(response, '<th>Active</th><td>True</td>', count=1)

    def test_view_indicates_future_activation_for_partner_with_active_after_in_future(self):
        self.skipTest('not implemented yet')

    def test_view_indicates_partner_is_active_with_active_after_in_past(self):
        self.skipTest('not implemented yet')

    def test_view_indicates_future_inactive_with_inactive_after_in_future(self):
        self.skipTest('not implemented yet')

    def test_view_indicates_disabled_for_partner_with_inactive_after_in_past(self):
        self.skipTest('not implemented yet')

    def test_view_displays_browsers_for_partner_config(self):
        self.skipTest('not implemented yet')

    def test_view_displays_scheduling_interval(self):
        self.skipTest('not implemented yet')


class BrowserViewTests(TestCase):
    def test_index_view_with_no_browsers(self):
        response = self.client.get(reverse('pik_check:browser_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No browsers are available.")
        self.assertQuerysetEqual(response.context['browser_list'], [])

    def test_index_view_with_a_browser(self):
        expected_browser = factories.BrowserFactory()
        response = self.client.get(reverse('pik_check:browser_index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['browser_list'], [repr(expected_browser)])


class BrowserDetailViewTests(TestCase):
    def test_detail_view_with_a_browser(self):
        browser = factories.BrowserFactory()
        response = self.client.get(reverse('pik_check:browser_detail', args=(browser.id,)))
        self.assertContains(response, browser.name, status_code=200)


class ScheduledJobModelTests(TestCase):
    def test_is_on_hold_for_date_in_past_is_false(self):
        p = factories.PartnerFactory()
        b = factories.BrowserFactory()
        scheduled_job = models.ScheduledJob(partner=p, browser=b)
        delta = datetime.timedelta(minutes=1)
        scheduled_job.hold_until = scheduled_job.hold_until - delta  # one minute ago
        scheduled_job.save()
        self.assertFalse(scheduled_job.is_on_hold())


class PartnerStatusViewTests(TestCase):
    pass


class PartnerStatusDetailViewTests(TestCase):
    pass
