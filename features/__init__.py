'''
    django-features
    ~~~~~~~~~~~~~~~

    Basic Django app to ease projects' roadmaps publishing.

    :copyright: (c) 2009-2011 by Pavlo Kapyshin.
    :license: BSD, see LICENSE for more details.
'''


__version__ = '0.2'
__author__ = 'Pavlo Kapyshin (admin@93z.org)'


from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from django.conf import settings

from models import Feature


DEFAULT_FEATURES_APP = 'features'


def get_features_app():
    features_app = get_features_app_name()

    if features_app not in settings.INSTALLED_APPS:
        raise ImproperlyConfigured(
            'The FEATURES_APP (%s) must be in INSTALLED_APPS' % features_app
        )

    try:
        pkg = import_module(features_app)
    except ImportError:
        raise ImproperlyConfigured(
            'The FEATURES_APP setting refers to a non-existing package.'
        )

    return pkg


def get_features_app_name():
    return getattr(settings, 'FEATURES_APP', DEFAULT_FEATURES_APP)


def get_model():
    app = get_features_app()
    
    if get_features_app_name() != DEFAULT_FEATURES_APP and hasattr(app, 'get_model'):
        return app.get_model()
    return Feature
