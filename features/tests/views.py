from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils.simplejson import loads

from features.models import Feature


class ApiTest(TestCase):
    urls = 'features.tests.api_urls'

    def setUp(self):
        self.site = Site.objects.get_current()
        self.data = {
            'title': 'Test title',
            'description': 'My description.',
            'site': self.site,
        }
        self.user = User.objects.create(username='Username')

    def check_feature(self, d, users, feature, site=None):
        site = site or self.site
        data = {
            'title': feature.title,
            'description': feature.description,
            'site': site.id,
            'people': [u.get_full_name() or u.username for u in users],
            'id': feature.id,
            'status': feature.status,
            'is_ready': feature.is_ready,
            'is_launched': feature.is_launched,
            'is_stopped': feature.is_stopped,
            'progress': feature.progress,
        }
        self.assertEqual(d, data)

    def test_list_features(self):
        url = reverse('list_features')
        response = loads(self.client.get(url).content)
        self.assertEqual(response, [])

        feature = Feature.objects.create(**self.data)
        feature.people.add(self.user)
        feature.save()

        response = loads(self.client.get(url).content)
        self.assertEqual(len(response), 1)
        self.check_feature(response[0], [self.user], feature)

        site = Site.objects.create(name='Test', domain='test.com')
        
        other_feature = Feature.objects.create(**dict(self.data, **{'site': site}))
        other_feature.people.add(self.user)
        other_feature.save()

        response = loads(self.client.get(url).content)
        self.assertEqual(len(response), 2)
        self.check_feature(response[0], [self.user], feature)
        self.check_feature(response[1], [self.user], other_feature, site=site)

    def test_list_features_for_site(self):
        url = reverse('list_features_for_site', kwargs={'site_id': self.site.id})
        response = loads(self.client.get(url).content)
        self.assertEqual(response, [])

        user_data = {
            'username': 'myusername',
            'first_name': 'Test',
            'last_name': 'Testovich',
        }
        user = User.objects.create(**user_data)

        site = Site.objects.create(name='Test', domain='test.com')

        feature = Feature.objects.create(**dict(self.data, **{'progress': 100}))
        feature.people.add(user)
        feature.save()
        
        other_feature = Feature.objects.create(**dict(self.data, **{'site': site}))
        other_feature.people.add(user)
        other_feature.save()

        response = loads(self.client.get(url).content)
        self.assertEqual(len(response), 1)
        self.check_feature(response[0], [user], feature)

        other_url = reverse('list_features_for_site', kwargs={'site_id': site.id})
        response = loads(self.client.get(other_url).content)
        self.assertEqual(len(response), 1)
        self.check_feature(response[0], [user], other_feature, site=site)

    def test_show_feature_details(self):
        feature = Feature.objects.create(**self.data)
        feature.people.add(self.user)
        feature.save()

        url = reverse('show_feature_details', kwargs={'feature_id': feature.id})
        response = loads(self.client.get(url).content)

        self.check_feature(response, [self.user], feature)

    def test_views_with_customized_fields(self):
        expected = {
            'title': self.data['title'],
            'description': self.data['description'],
        }
        feature = Feature.objects.create(**self.data)
        feature.people.add(self.user)
        feature.save()

        data2 = dict(self.data, **{'title': 'Other title', 'description': ''})
        expected2 = {
            'title': data2['title'],
            'description': data2['description'],
        }
        
        feature2 = Feature.objects.create(**data2)
        feature2.people.add(self.user)
        feature2.save()

        url = reverse('list_features_arg')
        response = loads(self.client.get(url).content)
        self.assertEqual(response, [expected, expected2])

        url = reverse('list_features_for_site_arg', kwargs={'site_id': self.site.id})
        response = loads(self.client.get(url).content)
        self.assertEqual(response, [expected, expected2])

        url = reverse('show_feature_details_arg', kwargs={'feature_id': feature.id})
        response = loads(self.client.get(url).content)
        self.assertEqual(response, expected)

        url = reverse('show_feature_details_arg', kwargs={'feature_id': feature2.id})
        response = loads(self.client.get(url).content)
        self.assertEqual(response, expected2)

