import pytest
from pytest_factoryboy import register

from ckanext.issues import model
from ckan.tests.factories import CKANFactory
import ckan.tests.helpers as helpers

class Issue(CKANFactory):
    class Meta:
        model = model.Issue
        action = 'issue_create'

    @classmethod
    def api_create(cls, data_dict):
        """Create entity via API call."""
        title = data_dict.get('title', None)
        if title is None:
            title = 'Test issue'
            data_dict['title'] = title
        data_dict = cls._api_prepare_args(data_dict)
        result = helpers.call_action(cls._meta.action, **data_dict)
        return cls._api_postprocess_result(result)

class IssueComment(CKANFactory):
    class Meta:
        model = model.IssueComment
        action = 'issue_comment_create'


@pytest.fixture()
def clean_db(reset_db, migrate_db_for):
    reset_db()
    migrate_db_for("issues")
