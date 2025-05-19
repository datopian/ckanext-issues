[![CI Actions Status](https://github.com/keitaroinc/ckanext-issues/workflows/CI/badge.svg)](https://github.com/keitaroinc/ckanext-issues/actions) [![Coverage Status](https://coveralls.io/repos/github/keitaroinc/ckanext-issues/badge.svg?branch=master)](https://coveralls.io/github/keitaroinc/ckanext-issues?branch=master) [![Pypi](https://img.shields.io/pypi/v/ckanext-issues)](https://pypi.org/project/ckanext-issues) [![Python](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue)](https://www.python.org) [![CKAN](https://img.shields.io/badge/ckan-2.9-red)](https://www.ckan.org)
# CKAN Issues Extension

This extension allows users to to report issues with datasets in a CKAN
instance.

## Requirements

This extension works with CKAN 2.9+.

## Installation

To install the plugin, enter your virtualenv and install from pip or source:

    pip install ckanext-isssues
   
    pip install -e git+http://github.com/keitaroinc/ckanext-issues

Create the necessary tables:

    ckan -c path-to/ckan.ini issuesdb

This will also register a plugin entry point, so you now should be
able to add the following to your CKAN .ini file::

    ckan.plugins = issues

After you clear your cache and restart the web server, the Issues extension
should be available.

## Upgrade from older versions

When upgrading ckanext-issues from older code versions, you should run the issues upgrade command, in case there are any model migrations (e.g. 11th Jan 2016):

    ckan -c path-to/ckan.ini issuesupdate

## What it does

Once installed and enabled, the issues extension will make available a per-
dataset issue tracker.

The issue tracker user interface can be found at:

    /dataset/{dataset-name-or-id}/issues

You can add an issue at:

    /dataset/{dataset-name-or-id}/issues/new


## API Documentation

The following API actions are provided by this extension. All endpoints are available under `/api/3/action/` and require appropriate authorization (API key in the Authorization header).

### /api/3/action/issue_show
Return a single issue/discussion.
- **Parameters:**
  - `dataset_id` (string): Dataset name or id
  - `issue_number` (string): Issue number
  - `include_reports` (bool, optional): Include abuse reports
- **Returns:** Dictionary with issue details

### /api/3/action/issue_create
Create a new issue/discussion.
- **Parameters:**
  - `title` (string): Title
  - `description` (string, optional): Description
  - `dataset_id` (string): Dataset name or id
- **Returns:** Dictionary with created issue

### /api/3/action/issue_update
Update an existing issue/discussion.
- **Parameters:**
  - `title` (string): Title
  - `description` (string, optional): Description
  - `dataset_id` (string): Dataset name or id
  - `issue_number` (int): Issue number
- **Returns:** Dictionary with updated issue

### /api/3/action/issue_delete
Delete an issue/discussion.
- **Parameters:**
  - `dataset_id` (string): Dataset name or id
  - `issue_number` (int): Issue number
- **Returns:** `{success: True}`

### /api/3/action/issue_search
Search issues/discussions.
- **Parameters:**
  - `dataset_id` (string, optional): Dataset name or id
  - `organization_id` (string, optional): Organization id
  - `include_sub_organizations` (bool, optional)
  - `q` (string, optional): Query string (searches titles)
  - `sort` (string, optional): 'newest', 'oldest', 'most_commented', etc.
  - `limit` (int, optional)
  - `offset` (int, optional)
  - `visibility` (string, optional): 'visible', 'hidden', ''
  - `include_datasets` (bool, optional)
  - `include_count` (bool, optional)
  - `include_results` (bool, optional)
- **Returns:** `{count: int, results: [issue_dict, ...]}`

### /api/3/action/issue_count
Count issues/discussions. (Alias for issue_search with `include_count=true` and `include_results=false`)
- **Parameters:** Same as `issue_search`
- **Returns:** `{count: int}`

### /api/3/action/issue_comment_create
Add a comment to an issue/discussion.
- **Parameters:**
  - `comment` (string): Comment text
  - `issue_number` (int): Issue number
  - `dataset_id` (string): Dataset name or id
- **Returns:** Dictionary with created comment

### /api/3/action/issue_report
Report an issue/discussion as abuse/spam.
- **Parameters:**
  - `dataset_id` (string): Dataset name or id
  - `issue_number` (int): Issue number
- **Returns:** Abuse report info (dict)

### /api/3/action/issue_report_clear
Clear abuse reports on an issue/discussion.
- **Parameters:**
  - `dataset_id` (string): Dataset name or id
  - `issue_number` (int): Issue number
- **Returns:** `True` on success

### /api/3/action/issue_comment_report
Report a comment as abuse/spam.
- **Parameters:**
  - `comment_id` (string): Comment id
- **Returns:** Abuse report info (dict)

### /api/3/action/issue_comment_report_clear
Clear abuse reports on a comment.
- **Parameters:**
  - `dataset_id` (string): Dataset name or id
  - `comment_id` (int): Comment id
- **Returns:** `True` on success

### /api/3/action/issue_report_show
Fetch abuse reports for an issue/discussion.
- **Parameters:**
  - `dataset_id` (string): Dataset name or id
  - `issue_number` (int): Issue number
- **Returns:** List of user ids who reported

### /api/3/action/issue_comment_search
Search comments (optionally only hidden ones).
- **Parameters:**
  - `organization_id` (string, optional): Organization id
  - `only_hidden` (bool, optional): Only hidden comments
- **Returns:** List of comment dicts

## Configuration

To switch-on notifications, you should set the following option in your
configuration, and all users in the group will get the email.

    ckanext.issues.send_email_notifications = true

If you set max_strikes then users can 'report' a comment as spam/abuse. If the number of users reporting a particular comment hits the max_strikes number then it is hidden, pending moderation.

    ckanext.issues.max_strikes = 2

### Activation

By default, issues are enabled for all datasets. If you wish to restrict
issues to specific datasets or organizations, you can use these config options:
    
    ckanext.issues.enabled_for_datasets = mydataset1 mydataset2 ...
    ckanext.issues.enabled_for_organizations = department-of-transport health-regulator

Alternatively, you can switch issues on/off for particular datasets by using an extra field:

    'issues_enabled': True

and you can set the default for all the other datasets (without that extra field):

    ckanext.issues.enabled_without_extra = false

For the extra field to work you must not set `enabled_per_dataset` or `enabled_for_organizations` options.

## Feedback

Please open an issue in the github [issue tracker][issues].

[issues]: https://github.com/keitaroinc/ckanext-issues

## Developers

Normal requirements for CKAN Extensions (including an installation of CKAN and
its dev requirements). Contributions welcome.

### Testing with Postgres
To run full production tests on postgres run. These are the tests that git actions will run

    pytest --ckan-ini=test.ini ckanext/issues/tests

