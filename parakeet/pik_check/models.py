from __future__ import unicode_literals

import django.utils.timezone
from django.core import urlresolvers
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
    scheduling_interval = models.PositiveSmallIntegerField(default=0)

    def __unicode__(self):
        return 'partner: %s, browsers: %s, enabled: %s, interval: %s minutes' % (
            self.partner.code,
            self.browsers.all(),
            self.enabled,
            self.scheduling_interval
        )

    def get_absolute_url(self):
        return urlresolvers.reverse('job_configuration_detail', kwargs={'pl': self.pk})


class ScheduledJob(models.Model):
    partner = models.ForeignKey('Partner', on_delete=models.CASCADE, blank=False, null=False)
    browser = models.ForeignKey('Browser', on_delete=models.CASCADE, blank=False, null=False)
    hold_until = models.DateTimeField(default=django.utils.timezone.now)
    dispatched = models.BooleanField(default=False)

    def __unicode__(self):
        return 'partner: %s, browser: %s, can run after %s, dispatched: %s' % (
            self.partner,
            self.browser,
            self.hold_until,
            self.dispatched
        )

    def is_on_hold(self):
        return self.hold_until > django.utils.timezone.now()
    is_on_hold.boolean = True

    def hold_for_timedelta(self, delta):
        self.hold_until = django.utils.timezone.now() + delta
        self.dispatched = False
        self.full_clean()
        self.save()


class CheckStage(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)
    identifier = models.CharField(max_length=16, null=False, blank=False, unique=True)
    ordering = models.PositiveSmallIntegerField(null=False, blank=False, unique=True)

    class Meta:
        ordering = ['ordering']

    def __unicode__(self):
        return '{name} ({identifier})'.format(name=self.name, identifier=self.identifier)


class CheckStageResult(models.Model):
    stage = models.ForeignKey('CheckStage', blank=False, null=False)
    run = models.ForeignKey('CheckRunResult', blank=False, null=False)
    successful = models.BooleanField(default=False)
    message = models.TextField(null=True, blank=False)


class CheckRunResult(models.Model):
    partner = models.ForeignKey('Partner', on_delete=models.CASCADE, blank=False, null=False)
    browser = models.ForeignKey('Browser', on_delete=models.CASCADE, blank=False, null=False)
    start_time = models.DateTimeField()
    completion_time = models.DateTimeField()
    successful = models.BooleanField(default=False)

    def __unicode__(self):
        return '{partner_code}, {browser}'.format(partner_code=self.partner.code, browser=self.browser)

    @property
    def duration(self):
        return self.completion_time - self.start_time
