import sys
from types import ModuleType

from django import template


register = template.Library()


class PeopleNamesNode(template.Node):

    def __init__(self, feature, var_name):
        self.feature = template.Variable(feature)
        self.var_name = var_name

    def render(self, ctx):
        try:
            feature = self.feature.resolve(ctx)
        except template.VariableDoesNotExist:
            return ''

        ctx[self.var_name] = feature.get_names()

        return ''


@register.tag
def get_people_names(parser, token):
    '''Add list of feature-related people's names to context.'''
    try:
        tag_name, for_, feature, as_, var_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            'Tag usage: {% %s for feature as var_name %}'
            % (token.contents.split()[0], )
        )

    if for_ != 'for':
        raise template.TemplateSyntaxError('Second argument must be \'for\'')

    if as_ != 'as':
        raise template.TemplateSyntaxError('Fourth argument must be \'as\'')

    return PeopleNamesNode(feature, var_name)


_locals = locals().copy()

sys.modules['features.templatetags.features'] = \
    features = ModuleType('features')

for k, v in _locals.iteritems():
    setattr(features, k, v)
