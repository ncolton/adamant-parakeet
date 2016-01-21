from __future__ import absolute_import
import random

import django.utils.timezone
from time import sleep
from celery import shared_task
from datetime import timedelta
from . import models

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def schedule_configured_jobs():
    jobs_updated = 0
    jobs_created = 0
    for job_configuration in models.JobConfiguration.objects.exclude(enabled=False):
        for browser in job_configuration.browsers.all():
            try:
                job = models.ScheduledJob.objects.get(partner=job_configuration.partner, browser=browser)
            except models.ScheduledJob.DoesNotExist:
                models.ScheduledJob.objects.create(partner=job_configuration.partner, browser=browser)
                jobs_created += 1
            else:
                if job.dispatched and not job.is_on_hold():
                    job.hold_for_timedelta(timedelta(minutes=job_configuration.scheduling_interval))
                    jobs_updated += 1

    logger.info('updated: %s, created: %s', jobs_updated, jobs_created)
    return {'updated': jobs_updated, 'created': jobs_created}


@shared_task
def dispatch_scheduled_jobs():
    job_expiration_in_seconds = 300  # 5 minutes

    scheduled_jobs = models.ScheduledJob.objects.filter(
        dispatched=False
    ).filter(
        hold_until__lt=django.utils.timezone.now()
    )

    logger.info('jobs to dispatch: %s', len(scheduled_jobs))
    for scheduled_job in scheduled_jobs:
        run_pik_check.apply_async(
            (scheduled_job.partner.code, scheduled_job.browser.name),
            queue='pik_check',
            expires=job_expiration_in_seconds
        )
        scheduled_job.dispatched = True
        scheduled_job.save()
    return len(scheduled_jobs)


class Stage(object):
    def __init__(self, identifier, successful, message=None):
        self.identifier = identifier
        self.successful = successful
        self.message = message


class CheckRun(object):
    def __init__(self, partner_code, browser_name):
        self._partner_code = partner_code
        self._browser_name = browser_name
        self.stage_results = []
        self.successful = False

    @property
    def partner_code(self):
        return self._partner_code

    @property
    def browser_name(self):
        return self._browser_name

    def start(self):
        self.start_time = django.utils.timezone.now()

    def complete(self):
        self.end_time = django.utils.timezone.now()

    def add_stage_result(self, stage_result):
        self.stage_results.append(stage_result)


@shared_task
def run_pik_check(partner_code, browser_name):
    results = CheckRun(partner_code=partner_code, browser_name=browser_name)
    results.start()

    for stage in ['pre-sso-check', 'load-partner-url', 'locate-sr-div', 'log-in', 'sso-confirmed']:
        result = True
        if random.randint(1, 100) > 80:
            result = False
        results.add_stage_result(Stage(identifier=stage, successful=result))
        if not result:
            break

    delay_seconds = random.randint(30, 180)

    logger.info('%s %s sleeping for %s seconds', partner_code, browser_name, delay_seconds)
    sleep(delay_seconds)
    results.complete()
    results.successful = results.stage_results[-1].successful

    store_pik_check_results(results)

    logger.info('pik check result for %s %s: %s', partner_code, browser_name, results.successful)
    return {'partner': partner_code, 'browser': browser_name, 'success': results.successful}


def store_pik_check_results(check_run):
    partner = models.Partner.objects.get(code=check_run.partner_code)
    browser = models.Browser.objects.get(name=check_run.browser_name)
    check_result = models.CheckRunResult(
        partner=partner,
        browser=browser,
        start_time=check_run.start_time,
        completion_time=check_run.end_time,
        successful=check_run.successful
    )
    check_result.save()

    for stage in check_run.stage_results:
        check_stage = models.CheckStage.objects.get(identifier=stage.identifier)
        stage_result = models.CheckStageResult(
            stage=check_stage,
            run=check_result,
            successful=stage.successful,
            message=stage.message
        )
        stage_result.save()
