from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from features.models import Feature


class FeatureModelTest(TestCase):

    def setUp(self):
        self.site = Site.objects.get_current()

    def test_creation(self):
        self.assertEqual(Feature.objects.count(), 0)
        
        f = Feature(
            title='Test title',
            description='Test description.',
            site=self.site,
        )
        f.save()

        self.assertEqual(Feature.objects.count(), 1)

        f2 = Feature.objects.create(
            title='Another feature',
            description='Test description again.',
            site=self.site,
        )
        
        self.assertEqual(Feature.objects.count(), 2)

    def test_defaults(self):
        f = Feature.objects.create(
            title='Some feature',
            description='Test description.',
            site=self.site,
        )

        self.assertEqual(f.progress, 0)
        self.assertEqual(f.is_launched, False)
        self.assertEqual(f.is_stopped, False)
        self.assertEqual(f.people.count(), 0)
        self.assertEqual(f.status, '')

    def test_is_ready(self):
        f = Feature.objects.create(
            title='Some feature',
            description='Test description.',
            site=self.site,
        )

        self.assertEqual(f.is_ready, False)

        f.progress = 50
        f.save()

        self.assertEqual(f.is_ready, False)

        f.progress = 100
        f.save()

        self.assertEqual(f.is_ready, True)

        f.progress = 5
        f.save()

        self.assertEqual(f.is_ready, False)

    def test_managers(self):
        f = Feature.objects.create(
            title='Some feature',
            description='Test description.',
            site=self.site,
        )

        # Ready.
        self.assertEqual(Feature.ready.count(), 0)

        f.progress = 100
        f.save()
        
        self.assertEqual(Feature.ready.count(), 1)
        self.assertEqual(Feature.ready.all()[0], f)
        
        self.assertEqual(Feature.launched.count(), 0)
        self.assertEqual(Feature.stopped.count(), 0)

        # Launched.
        f.is_launched = True
        f.save()

        self.assertEqual(Feature.ready.count(), 1)
        self.assertEqual(Feature.ready.all()[0], f)

        self.assertEqual(Feature.launched.count(), 1)
        self.assertEqual(Feature.launched.all()[0], f)

        self.assertEqual(Feature.stopped.count(), 0)
        
        # Stopped.
        f.is_stopped = True
        f.save()

        self.assertEqual(Feature.ready.count(), 1)
        self.assertEqual(Feature.ready.all()[0], f)

        self.assertEqual(Feature.launched.count(), 1)
        self.assertEqual(Feature.launched.all()[0], f)

        self.assertEqual(Feature.stopped.count(), 1)
        self.assertEqual(Feature.stopped.all()[0], f)

    def test_get_names(self):
        username = 'TestUserName'
        obj = Feature.objects.create()
        user = User.objects.create(username=username)
        obj.people.add(user)
        obj.save()

        names = obj.get_names()
        self.assertEqual(len(names), 1)
        self.assertEqual(names[0], username)

        username2, fn2, ln2 = 'user2name', 'Name2', 'Last2'
        user2 = User.objects.create(
            username=username2,
            first_name=fn2,
            last_name=ln2,
        )
        obj.people.add(user2)

        names = obj.get_names()
        self.assertEqual(len(names), 2)
        self.assertEqual(names, [username, ' '.join((fn2, ln2))])

