import pytest

from ckan.tests import factories

from ckanext.issues.tests import factories as issue_factories
from ckanext.issues.lib.util import issue_count, issue_comments, issue_comment_count
from ckanext.issues.tests.fixtures import issues_setup

@pytest.mark.usefixtures("with_plugins")
class TestUtils(object):

    @pytest.mark.usefixtures("clean_db", "issues_setup", "with_plugins", "test_request_context")
    def test_issue_count(self):
        user = factories.User()
        org = factories.Organization()
        dataset = factories.Dataset(owner_org=org['id'])
        issue = issue_factories.Issue(title='Test Issue', description='Some description', dataset_id=dataset['id'], user_id=user['id'])
        assert issue_count(dataset) == 1

    @pytest.mark.usefixtures("clean_db", "issues_setup", "with_plugins", "test_request_context")
    def test_issue_comment_count(self):
        user = factories.User()
        org = factories.Organization()
        dataset = factories.Dataset(owner_org=org['id'])
        issue = issue_factories.Issue(title='Test Issue', description='Some description', dataset_id=dataset['id'], user_id=user['id'])
        comment1 = issue_factories.IssueComment(
                    issue_number=issue['number'],
                    dataset_id=issue['dataset_id'],
        )
        comment2 = issue_factories.IssueComment(
                    issue_number=issue['number'],
                    dataset_id=issue['dataset_id'],
        )
        comment3 = issue_factories.IssueComment(
                    issue_number=issue['number'],
                    dataset_id=issue['dataset_id'],
        )
        assert issue_comment_count(issue) == 3

    @pytest.mark.usefixtures("clean_db", "issues_setup", "with_plugins", "test_request_context")
    def test_issue_comments(self):
        user = factories.User()
        org = factories.Organization()
        dataset = factories.Dataset(owner_org=org['id'])
        issue = issue_factories.Issue(title='Test Issue', description='Some description', dataset_id=dataset['id'], user_id=user['id'])
        comment1 = issue_factories.IssueComment(
                    issue_number=issue['number'],
                    dataset_id=issue['dataset_id'],
        )
        comment2 = issue_factories.IssueComment(
                    issue_number=issue['number'],
                    dataset_id=issue['dataset_id'],
        )
        comment3 = issue_factories.IssueComment(
                    issue_number=issue['number'],
                    dataset_id=issue['dataset_id'],
        )
        comments_is = issue_comments(issue)
        assert [comment1['id'], comment2['id'], comment3['id']] ==\
               [comment.id for comment in comments_is]
