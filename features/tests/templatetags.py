try:
    from cStringIO import StringIO as SIO
except ImportError:
    from StringIO import StringIO as SIO

from django.db import models
from django.test import TestCase
from django.template import Template, Context
from django.contrib.auth.models import User

from features.models import Feature


class GetPeopleNamesTest(TestCase):

    def setUp(self):
        self.tmpl = Template(
            u'{% load features %}{% get_people_names for obj as names %}'
            u'{{ names|join:", " }}'
        )
    
    def runTest(self):
        username = 'TestUserName'
        obj = Feature.objects.create()
        user = User.objects.create(username=username)
        obj.people.add(user)
        obj.save()

        rendered = self.tmpl.render(Context({'obj': obj}))
        self.assertEqual(rendered, username)

        username2, fn2, ln2 = 'SecondUsername', 'Name', 'Lname'
        user2 = User.objects.create(
            username=username2,
            first_name=fn2,
            last_name=ln2,
        )
        obj.people.add(user2)
        obj.save()

        rendered = self.tmpl.render(Context({'obj': obj}))
        expected = ', '.join((username, ' '.join((fn2, ln2))))
        self.assertEqual(rendered, expected)
