from __future__ import unicode_literals

from django.db import models


class JobConfiguration(models.Model):
    partner = models.ForeignKey('partners.Partner', on_delete=models.CASCADE, blank=False, null=False)
    browsers = models.ManyToManyField('browsers.Browser')
    enabled = models.BooleanField(default=False)
    scheduling_interval = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return 'Job Configuration for %s, browsers: %s, enabled: %s' % (self.partner.code, self.browsers, self.enabled)
