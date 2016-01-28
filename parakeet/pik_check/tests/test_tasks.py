from __future__ import absolute_import
from django.test import TestCase
from .. import tasks
from .. import models
from . import factories
import django.utils.timezone
import datetime


class JobSchedulingTests(TestCase):
    def test_no_jobs_scheduled_if_no_partners(self):
        result = tasks.schedule_jobs()
        self.assertEqual(models.ScheduledJob.objects.count(), 0)

    def test_no_jobs_scheduled_if_no_active_partners(self):
        partner = factories.PartnerFactory()
        self.assertFalse(partner.is_active)
        self.assertEqual(models.ScheduledJob.objects.count(), 0)

    def test_one_job_scheduled_if_one_active_partner_with_one_browser(self):
        expected_statistics = {
            'created': 1,
            'updated': 0,
            'unaltered': 0
        }
        partner = factories.PartnerFactory()
        browser = factories.BrowserFactory()
        partner.browsers.add(browser)
        partner.active_after = django.utils.timezone.now().date() - datetime.timedelta(days=1)
        partner.save()
        self.assertTrue(partner.is_active)
        statistics = tasks.schedule_jobs()
        self.assertDictEqual(statistics, expected_statistics)
        self.assertEqual(models.ScheduledJob.objects.count(), expected_statistics['created'])

    def test_one_job_per_browser_scheduled_with_one_partner(self):
        expected_statistics = {
            'created': 3,
            'updated': 0,
            'unaltered': 0
        }
        partner = factories.PartnerFactory()
        for _ in range(3):
            partner.browsers.add(factories.BrowserFactory())
        partner.active_after = django.utils.timezone.now().date() - datetime.timedelta(days=1)
        partner.save()
        self.assertTrue(partner.is_active)
        statistics = tasks.schedule_jobs()
        self.assertDictEqual(statistics, expected_statistics)
        self.assertEqual(models.ScheduledJob.objects.count(), expected_statistics['created'])

    def test_one_job_per_browser_with_multiple_partners(self):
        expected_statistics = {
            'created': 6,
            'updated': 0,
            'unaltered': 0
        }
        partner = factories.PartnerFactory()
        for _ in range(3):
            partner.browsers.add(factories.BrowserFactory())
        partner.active_after = django.utils.timezone.now().date() - datetime.timedelta(days=1)
        partner.save()
        self.assertTrue(partner.is_active)
        partner = factories.PartnerFactory()
        for _ in range(3):
            partner.browsers.add(factories.BrowserFactory())
        partner.active_after = django.utils.timezone.now().date() - datetime.timedelta(days=1)
        partner.save()
        self.assertTrue(partner.is_active)
        statistics = tasks.schedule_jobs()
        self.assertDictEqual(statistics, expected_statistics)
        self.assertEqual(models.ScheduledJob.objects.count(), expected_statistics['created'])
