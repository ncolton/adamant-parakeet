from __future__ import unicode_literals

from django.db import models


class Browser(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)

    def __unicode__(self):
        return 'Browser: %s' % self.name
