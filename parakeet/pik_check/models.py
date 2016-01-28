from __future__ import unicode_literals
from django.core.exceptions import ValidationError

import django.utils.timezone
from django.core import urlresolvers
from django.db import models
from django.utils.translation import ugettext_lazy as _
from . import validators
import datetime


class Partner(models.Model):
    code = models.CharField(max_length=20, null=False, blank=False, unique=True,
                            validators=[validators.validate_uppercase])
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)
    active_after = models.DateField(null=True, blank=True)
    inactive_after = models.DateField(null=True, blank=True)
    browsers = models.ManyToManyField('Browser')
    scheduling_interval = models.DurationField(default=datetime.timedelta(minutes=0))

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.code)

    @property
    def is_active(self):
        if not self.active_after:
            return False

        if self.inactive_after:
            if self.inactive_after < django.utils.timezone.now().date():
                return False

        if self.active_after < django.utils.timezone.now().date():
            return True
        else:
            return False

    def clean(self):
        if self.inactive_after and self.active_after:
            if self.inactive_after < self.active_after:
                raise ValidationError(_('Deactivation date cannot be before the activation date.'))

        if len(''.join(self.code.split())) == 0:
            raise ValidationError(_('Partner code must be non-blank'))


class Browser(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)

    def __unicode__(self):
        return '%s' % self.name


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
