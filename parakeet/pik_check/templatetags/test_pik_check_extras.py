from __future__ import absolute_import
from django.test import TestCase
from datetime import timedelta
from . import pik_check_extras


class NaturalTimeDeltaTestCase(TestCase):
    def test_one_second(self):
        delta = timedelta(seconds=1)
        self.assertEqual(pik_check_extras.naturalTimeDelta(delta), '1 second')

    def test_just_seconds(self):
        delta = timedelta(seconds=42)
        self.assertEqual(pik_check_extras.naturalTimeDelta(delta), '42 seconds')

    def test_one_minute(self):
        delta = timedelta(seconds=60)
        self.assertEqual(pik_check_extras.naturalTimeDelta(delta), '1 minute')

    def test_just_minutes(self):
        delta = timedelta(minutes=42)
        self.assertEqual(pik_check_extras.naturalTimeDelta(delta), '42 minutes')

    def test_minutes_and_seconds(self):
        delta = timedelta(minutes=42, seconds=42)
        self.assertEqual(pik_check_extras.naturalTimeDelta(delta), '42 minutes 42 seconds')

    def test_one_hour(self):
        delta = timedelta(hours=1)
        self.assertEqual(pik_check_extras.naturalTimeDelta(delta), '1 hour')

    def test_hours(self):
        delta = timedelta(hours=2)
        self.assertEqual(pik_check_extras.naturalTimeDelta(delta), '2 hours')

    def test_hours_minutes_and_seconds(self):
        delta = timedelta(hours=2, minutes=42, seconds=42)
        self.assertEqual(pik_check_extras.naturalTimeDelta(delta), '2 hours 42 minutes 42 seconds')

    def test_day(self):
        delta = timedelta(days=1)
        self.assertEqual(pik_check_extras.naturalTimeDelta(delta), '1 day')

    def test_day(self):
        delta = timedelta(days=2)
        self.assertEqual(pik_check_extras.naturalTimeDelta(delta), '2 days')
