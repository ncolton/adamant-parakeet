from __future__ import unicode_literals

from django.db import models


class Partner(models.Model):
    code = models.CharField(max_length=20, null=False, blank=False, unique=True)
    name = models.CharField(max_length=200, null=False, blank=False)

    def __unicode__(self):
        return 'Partner code: %s name: %s' % (self.code, self.name)
