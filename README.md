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

Iterate Job Configurations
	For each active
		for each permutation
			find existing record in scheduled jobs
				if dispatched and if `run after` time exceeded
					update entry with new `run after` value and reset dispatched flag
			if not in table
				create new entry

### Job Dispatcher

Responsible for creating a new job in the queue that will be consumed by a worker to run a PIK check.

For each Scheduled Job not dispatched
	If now > `run after`
		create a new PIK check job
		add it to the queue
		mark the Scheduled Job as dispatched
