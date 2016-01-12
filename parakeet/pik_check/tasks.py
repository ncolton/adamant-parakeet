from __future__ import absolute_import
import random

import django.utils.timezone
from time import sleep
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
    return {'updated': jobs_updated, 'created': jobs_created}


@shared_task
def dispatch_scheduled_jobs():
    job_expiration_in_seconds = 300  # 5 minutes

    scheduled_jobs = ScheduledJob.objects.filter(
        dispatched=False
    ).filter(
        hold_until__lt=django.utils.timezone.now()
    )

    logger.info('jobs to dispatch: %s', len(scheduled_jobs))
    for scheduled_job in scheduled_jobs:
        run_pik_check.apply_async(
            (scheduled_job.partner.code, scheduled_job.browser.name),
            queue='pik_checks',
            expires=job_expiration_in_seconds
        )
        scheduled_job.dispatched = True
        scheduled_job.save()
    return len(scheduled_jobs)


@shared_task
def run_pik_check(partner, browser):
    delay_seconds = random.randint(30, 180)
    result = random.choice(['Pass', 'Fail', 'Unstable'])

    logger.info('%s %s sleeping for %s seconds', partner, browser, delay_seconds)
    sleep(delay_seconds)
    logger.info('pik check result for %s %s: %s', partner, browser, result)
    return {'partner': partner, 'browser': browser, 'duration': delay_seconds, 'result': result}
