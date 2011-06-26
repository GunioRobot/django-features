#!/usr/bin/env python

import os.path as op
from distutils.core import setup


def read(fn):
    return open(op.join(op.dirname(__file__), fn), 'r').read()


setup(
    name='django-features',
    version='0.2.1',
    author='Pavlo Kapyshin',
    author_email='i@93z.org',
    license='New BSD',
    url='https://github.com/Kapishin/django-features',
    long_description=read('README'),
    packages=['features', 'features.tests', 'features.templatetags'],
    requires=['django'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries',
    ],
)

