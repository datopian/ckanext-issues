from ckanext.issues import model
from ckan.new_tests import factories, helpers

import factory

class Issue(factory.Factory):
    FACTORY_FOR = model.Issue

    title = 'Test issue'
    description = 'Some description'

    @classmethod
    def _build(cls, target_class, *args, **kwargs):
        raise NotImplementedError(".build() isn't supported in CKAN")

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        if args:
            assert False, "Positional args aren't supported, use keyword args."

        context = {'user': factories._get_action_user_name(kwargs)}

        # issue_create is so badly behaved I'm doing this for now
        data_dict = dict(**kwargs)
        data_dict.pop('user')

        issue_dict = helpers.call_action('issue_create',
                                           context=context,
                                           **data_dict)
        return issue_dict