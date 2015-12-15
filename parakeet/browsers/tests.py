from __future__ import unicode_literals
from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Browser


def create_browser(browser_name):
    return Browser.objects.create(name=browser_name)


class BrowserMethodTests(TestCase):
    def test_unicode_output(self):
        self.assertEqual(str(create_browser(u'Potato')), 'Browser: Potato')


class BrowserViewTests(TestCase):
    def test_index_view_with_no_browsers(self):
        response = self.client.get(reverse('browsers:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No browsers are available.")
        self.assertQuerysetEqual(response.context['browser_list'], [])

    def test_index_view_with_a_browser(self):
        expected_browser = create_browser('Foo Browser')
        response = self.client.get(reverse('browsers:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['browser_list'], [repr(expected_browser)])


class BrowserDetailViewTests(TestCase):
    def test_detail_view_with_a_browser(self):
        browser = create_browser(browser_name='Detailed Browser')
        response = self.client.get(reverse('browsers:detail', args=(browser.id,)))
        self.assertContains(response, browser.name, status_code=200)
