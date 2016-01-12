from __future__ import absolute_import

from celery import shared_task
from datetime import timedelta
from .models import JobConfiguration, ScheduledJob

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def schedule_configured_jobs():
    jobs_updated = 0
    jobs_created = 0
    for job_configuration in JobConfiguration.objects.exclude(enabled=False):
        for browser in job_configuration.browsers.all():
            try:
                job = ScheduledJob.objects.get(partner=job_configuration.partner, browser=browser)
            except ScheduledJob.DoesNotExist:
                ScheduledJob.objects.create(partner=job_configuration.partner, browser=browser)
                jobs_created = jobs_created + 1
            else:
                if job.dispatched and not job.is_on_hold():
                    job.hold_for_timedelta(timedelta(minutes=job_configuration.scheduling_interval))
                    jobs_updated = jobs_updated + 1

    logger.info('updated: %s, created: %s', jobs_updated, jobs_created)
