import json
import ckanext.issues.model as issue_model
import ckan.model as model
import ckan.plugins.toolkit as tk

_ = tk._
h = tk.h

def issue_count(package):
    return issue_model.Issue.get_issue_count_for_package(package['id'])

def issue_comment_count(issue):
    return issue_model.IssueComment.get_comment_count_for_issue(issue['id'])

def issue_comments(issue):
    return issue_model.IssueComment.get_comments_for_issue(issue['id'])


def _issue_query(org, resolved_required=False, days=None):
    r = "NOT" if resolved_required else ""
    e = ""
    if days:
        e = "AND extract(epoch from (now() - created)) > (82600 * {days})"\
            .format(days=days)

    q = """
        SELECT count(id)
        FROM "issue"
        WHERE {r} resolved is NULL
          {extra}
          AND package_id in (
            SELECT table_id
            FROM member
            WHERE group_id='{gid}'
              AND table_name='package'
              AND state='active'
          );
    """.format(gid=org.id, r=r, extra=e)

    return q

def old_unresolved(org, days=30):
    q = _issue_query(org, False, days=days)
    return model.Session.execute(q).scalar()

def resolved_count_for_organization(org):
    q = _issue_query(org, False)
    return model.Session.execute(q).scalar()

def unresolved_count_for_organization(org):
    q = _issue_query(org, True)
    return model.Session.execute(q).scalar()


# patch imported on ckan core "ckan/lib/activity_streams", plase check patch file.
# https://github.com/ckan/ckan/blob/ckan-2.8.2/ckan/lib/activity_streams.py#L123-L190
def get_snippet_issue(activity, detail):

    if activity['activity_type'] in ['issue closed', 'issue reopened']:
        issue_id = activity['data'].get('number')
    elif activity['activity_type'] == 'new issue':
        issue_id = activity['data'].get('id')
    elif activity['activity_type'] == 'changed issue':
        issue_id = activity['data'].get('issue_number')
    elif activity['activity_type'] == 'issue deleted':
        return 'a'
    else:
        return 'a'
    try:
        dataset_id = activity['data']['dataset_id']
        if activity['activity_type'] == 'changed issue':
            try:
                issue_dict =  tk.get_action('issue_show')({'ignore_auth': True}, 
                                {'issue_number': issue_id, 'dataset_id': dataset_id})
            except:
                issue_id = activity['data'].get('issue_id')
                issue_dict =  tk.get_action('issue_show')({'ignore_auth': True}, 
                                {'issue_number':  activity['data'].get('issue_id'), 'dataset_id': dataset_id})
        else:
            issue_dict =  tk.get_action('issue_show')({'ignore_auth': True}, 
                            {'issue_number': issue_id, 'dataset_id': dataset_id})
        url = h.url_for('issues_show', dataset_id=dataset_id, issue_number=issue_id)
        return  '<a href="%s">%s</a>' % (url, issue_dict['title'][0:30])
    except:
        # Log simple activity if the issue_id is not found
        return 'a'

def activity_stream_string_issue_change(context, activity):
    return _("{actor} commented on {issue} discussion")

def activity_stream_string_new_issue(context, activity):
    return _("{actor} started a new discussion on the dataset {dataset}")

def activity_stream_string_deleted_issue(context, activity):
    return _("{actor} deleted {issue} discussion on the dataset {dataset}")

def activity_stream_string_issue_closed(context, activity):
    return _("{actor} closed {issue} on the dataset {dataset}")

def activity_stream_string_issue_reopened(context, activity):
    return _("{actor} reopened {issue} on the dataset {dataset}")

