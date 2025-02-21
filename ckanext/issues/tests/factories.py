from ckanext.issues import model
from ckan.tests import factories
import ckan.plugins.toolkit as toolkit
import factory


class Issue(factory.Factory):
    class Meta:
        model = model.Issue
        abstract = False

    title = factory.Sequence(lambda n: f"Test Issue [{n}]")
    description = "Some description"
    dataset_id = factory.LazyAttribute(lambda _: factories.Dataset()["id"])
    # Add a default value for 'user' to avoid KeyError
    user = "testsysadmin"

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        if args:
            raise ValueError("Positional args aren't supported, use keyword args.")

        # Ensure 'user' is always present in kwargs
        user = kwargs.pop("user", "testsysadmin")
        context = {"user": user}

        data_dict = dict(**kwargs)

        try:
            issue_dict = toolkit.get_action("issue_create")(
                context, data_dict
            )
        except toolkit.ValidationError as e:
            raise ValueError(f"Validation Error: {e}") from e

        return issue_dict


class IssueComment(factory.Factory):
    class Meta:
        model = model.IssueComment
        abstract = False

    comment = "some comment"
    user = "testsysadmin"  # Default user for consistency

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        if args:
            raise ValueError("Positional args aren't supported, use keyword args.")

        # Ensure 'user' is always present in kwargs
        user = kwargs.pop("user", "testsysadmin")
        context = {"user": user}

        data_dict = dict(**kwargs)

        try:
            issue_comment_dict = toolkit.get_action("issue_comment_create")(
                context, data_dict
            )
        except toolkit.ValidationError as e:
            raise ValueError(f"Validation Error: {e}") from e

        return issue_comment_dict

