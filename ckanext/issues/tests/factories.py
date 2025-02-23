import pytest
from pytest_factoryboy import register

from ckanext.issues import model
from ckan.tests.factories import CKANFactory


class Issue(CKANFactory):
    class Meta:
        model = model.Issue
        action = 'issue_create'

class IssueComment(CKANFactory):
    class Meta:
        model = model.IssueComment
        action = 'issue_comment_create'


@pytest.fixture()
def clean_db(reset_db, migrate_db_for):
    reset_db()
    migrate_db_for("issues")
