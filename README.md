# Settings

Settings specific to the app *pik_check* should go in a dictionary specifically for it:

```python
PIK_CHECK = {
    'job_expiry': 60 * 3
}
```

## Bootstrap Styling configuration

Configuration for the Bootstrap framework needs to be in a dictionary specifically for it:

```python
BOOTSTRAP3 = {
    'include_jquery': True,
    'jquery_url': '//code.jquery.com/jquery-1.12.0.min.js'
}
```

Full documentation is available at http://django-bootstrap3.readthedocs.org/en/latest/settings.html

## Celery Settings

Full details on Celery configuration can be found at http://docs.celeryproject.org/en/latest/configuration.html

### Scheduling and Dispatching Configuration

The configuration should be similar to the following:

```python
CELERYBEAT_SCHEDULE = {
    'schedule-configured-jobs': {
        'task': 'pik_check.tasks.schedule_configured_jobs',
        'schedule': timedelta(seconds=30),
        'options': {
            'queue': 'scheduling'
        }
    },
    'dispatch-scheduled-jobs': {
        'task': 'pik_check.tasks.dispatch_scheduled_jobs',
        'schedule': timedelta(seconds=30),
        'options': {
            'queue': 'scheduling'
        }
    }
}
```

Adjusting the *timedelta* value will change how often these jobs are run. Running them frequently should avoid a large back log of tasks needing to be accomplished, ensuring a short run time and not falling behind.

### Task Queue, State, and Result storage

Indicate the storage to use by setting the `BROKER_URL` value.

Set the `CELERY_RESULT_BACKEND` to enable persisting the task state and return values.

### Time Zone

Ensure that `CELERY_ENABLE_UTC` agrees with the `USE_TZ` and `TIME_ZONE` settings.


# Running

## Daemons

### Beat Scheduler

To enable time-based task scheduling:

From the same directory as *manage.py* execute: `celery -A parakeet beat`

### Workers

From the same directory as *manage.py* execute…
* `celery -A parakeet worker --queues=scheduling --hostname=scheduling.%h` to process scheduling tasks.
* `celery -A parakeet worker --queues=pik_check --hostname=pik_check.%h` to process PIK Check jobs.

# Design Foo

Failures of a queued job should be infrastructure related, not site problems, and auto-retried?
For a job success that reports a native thread issue, inability to get a selenium session, etc. those need to be reclassified as job failures somehow. This is a code change to the actual PIK check, rather than to the management framework…


## Requirements

Want to be able to see quickly if a Partner log in is working
Want to be able to see quickly if a Partner log in SSO is working
Want to be able to differentiate infrastructure problems from problems with the partner

As a user

* I want to see a list of partners
* I want to add a new partner
* I want to see a list of browsers
* I want to add a new browser
* For a given partner
  * I want to add a Job Configuration
* I want to see scheduled jobs…
  * that are in the future?
  * not dispatched?
* I want to see a list of jobs whose `run after` time is past but are not yet dispatched


## Entities

### Partner
A partner we work with
- code
- name (human readable)
- enabled / active (maybe? can update occasionally with redshift table that has this info as well to auto-determine whether partner is active)

### Browser
Record referring to a web browser that is configured and available through the infrastructure.
- name
- icon

### Job Configuration
Specifying a partner and the configuration for what checks should be run and how often.
- Partner (reference)
- Browsers (references)
- scheduling interval (how long to wait between checking the partner)
- enabled? [ later, add in logic to record why something is disabled when it is being set disabled ]

Do we need these other things? Should these be properties of the Partner, rather than the job configuration?
- SSO check
- Express checkout enabled
- Wait override
- Entry point
- Custom product page

### Scheduled Job
The pairing of a partner and browser for which a PIK check should be run at some time.
- run after (timestamp after which the job can be run)
- partner (reference)
- browser (reference)
- dispatched to work queue?

### Job Result
The outcome of a PIK check against a Partner-Browser pairing.
- Partner
- Browser
- Executed at (timestamp / datetime)
- Duration (seconds elapsed for PIK check)
- Outcome

### Outcome Types
- Need to somehow categorize the outcomes from a PIK check into discrete, known types…
- Need to know if it is a success or a failure
- Need to differentiate between infrastructure failures and actual log in failures.


## System Components

### Job Scheduler

Responsible for creating a Scheduled Job based on enabled Job Configurations.

```
Iterate Job Configurations
	For each active
		for each permutation
			find existing record in scheduled jobs
				if dispatched and if `run after` time exceeded
					update entry with new `run after` value and reset dispatched flag
			if not in table
				create new entry
```

### Job Dispatcher

Responsible for creating a new job in the queue that will be consumed by a worker to run a PIK check.

```
For each Scheduled Job not dispatched
	If now > `run after`
		create a new PIK check job
		add it to the queue
		mark the Scheduled Job as dispatched
```
