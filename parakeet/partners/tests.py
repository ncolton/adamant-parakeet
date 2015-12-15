from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Partner


def create_partner(partner_code, partner_name):
    return Partner.objects.create(code=partner_code, name=partner_name)


class PartnerViewTests(TestCase):
    def test_index_view_with_no_partners(self):
        response = self.client.get(reverse('partners:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No partners are available.")
        self.assertQuerysetEqual(response.context['partner_list'], [])

    def test_index_view_with_a_partner(self):
        expected_partner = create_partner('foo', 'Foo Industries')
        response = self.client.get(reverse('partners:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['partner_list'], [repr(expected_partner)])


class PartnerDetailViewTests(TestCase):
    def test_detail_view_with_a_partner(self):
        partner = create_partner(partner_code='detpart', partner_name='Detailed Partner')
        response = self.client.get(reverse('partners:detail', args=(partner.id,)))
        self.assertContains(response, partner.name, status_code=200)
