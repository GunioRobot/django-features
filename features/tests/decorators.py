#-*- coding: utf-8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse

from features.decorators import as_json


class AsJsonTest(TestCase):
    urls = 'features.tests.as_json_urlviews'

    def test_dict(self):
        response = self.client.get(reverse('test_dict'))
        self.assertEqual(response.content, '{"greeting": "Hello, JSON!"}')

    def test_list(self):
        response = self.client.get(reverse('test_list'))
        self.assertEqual(response.content, '["Hello, JSON!", 123]')
