import factory
import random
import string


class BrowserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'pik_check.Browser'
        django_get_or_create = ('name',)

    name = factory.Iterator(['Chrome', 'Firefox', 'Internet Explorer', 'Opera', 'PhantomJS'])


class PartnerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'pik_check.Partner'

    name = factory.Faker('company')

    @factory.lazy_attribute
    def code(self):
        l = []
        for n in range(10):
            l.append(random.choice(string.uppercase))
        return ''.join(l)
