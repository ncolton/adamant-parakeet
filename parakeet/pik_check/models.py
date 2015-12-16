from __future__ import unicode_literals

from django.db import models


class Partner(models.Model):
    code = models.CharField(max_length=20, null=False, blank=False, unique=True)
    name = models.CharField(max_length=200, null=False, blank=False)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.code)


class Browser(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)

    def __unicode__(self):
        return '%s' % self.name


class JobConfiguration(models.Model):
    partner = models.ForeignKey('Partner', on_delete=models.CASCADE, blank=False, null=False)
    browsers = models.ManyToManyField('Browser')
    enabled = models.BooleanField(default=False)
    scheduling_interval = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return 'partner: %s, browsers: %s, enabled: %s, interval: %s minutes' % (
            self.partner.code,
            self.browsers.all(),
            self.enabled,
            self.scheduling_interval
        )
