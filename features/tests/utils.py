from django.db import models
from django.test import TestCase

from features.utils import get_name, get_field, obj_to_dict


class User(object):

    def __init__(self, username, full_name=u''):
        self.username = username
        self._full_name = full_name

    def get_full_name(self):
        return self._full_name.strip()


class GetNameTest(TestCase):

    def test_with_username_only(self):
        username = 'Testusername'
        u = User(username=username)
        self.assertEqual(get_name(u), username)

    def test_with_both_username_and_name(self):
        username, full_name = 'Testusername', 'Full User\'s name'
        u = User(username=username, full_name=full_name)
        self.assertEqual(get_name(u), full_name)


class RelationshipTestModel(models.Model):
    some_attr = 'Attribute value.'

    class Meta:
        app_label = 'features'


class TestModel(models.Model):
    test_attr = 'test attr value'

    some_field = models.CharField(default=u'test string', max_length=50)
    num_field = models.IntegerField(default=0)
    test_fk = models.ForeignKey(RelationshipTestModel, null=True,
                                related_name='fieldtests')
    test_m2m = models.ManyToManyField(RelationshipTestModel, null=True)

    class Meta:
        app_label = 'features'

    @property
    def test(self):
        return self.test_attr


class GetFieldTest(TestCase):

    def test_manager(self):
        other_obj = RelationshipTestModel.objects.create()
        obj = TestModel.objects.create()
        obj.test_m2m.add(other_obj)
        obj.save()

        name, value = get_field(('test_m2m', lambda o: o.some_attr), obj)
        self.assertEqual(name, 'test_m2m')
        self.assertEqual(value, ['Attribute value.'])

        name, value = get_field(('test_m2m', lambda o: o.id), obj)
        self.assertEqual(name, 'test_m2m')
        self.assertEqual(value, [other_obj.id])

    def test_foreign_key(self):
        fk_obj = RelationshipTestModel.objects.create()
        obj = TestModel.objects.create(test_fk=fk_obj)
        
        name, value = get_field(('test_fk', lambda o: o.some_attr), obj)
        self.assertEqual(name, 'test_fk')
        self.assertEqual(value, 'Attribute value.')

        name, value = get_field(('test_fk', lambda o: o.id), obj)
        self.assertEqual(name, 'test_fk')
        self.assertEqual(value, fk_obj.id)

    def test_attr(self):
        obj = TestModel.objects.create()
        name, value = get_field('test_attr', obj)
        self.assertEqual(name, 'test_attr')
        self.assertEqual(value, 'test attr value')

    def test_field(self):
        obj = TestModel.objects.create()
        name, value = get_field('some_field', obj)
        self.assertEqual(name, 'some_field')
        self.assertEqual(value, u'test string')

        num_name, num_value = get_field('num_field', obj)
        self.assertEqual(num_name, 'num_field')
        self.assertEqual(num_value, 0)

        obj = TestModel.objects.create(
            some_field='some text',
            num_field=435,
        )
        name, value = get_field('some_field', obj)
        self.assertEqual(name, 'some_field')
        self.assertEqual(value, u'some text')

        num_name, num_value = get_field('num_field', obj)
        self.assertEqual(num_name, 'num_field')
        self.assertEqual(num_value, 435)

    def test_property(self):
        obj = TestModel.objects.create()
        name, value = get_field('test', obj)
        self.assertEqual(name, 'test')
        self.assertEqual(value, 'test attr value')


class ObjToDictTest(TestCase):

    def test_with_fields(self):
        fk_obj = RelationshipTestModel.objects.create()
        m2m_obj = RelationshipTestModel.objects.create()
        obj = TestModel.objects.create(test_fk=fk_obj)
        obj.test_m2m.add(m2m_obj)
        obj.save()
        
        fields = (
            'test_attr',
            'some_field',
            ('test_fk', lambda o: o.id),
            ('test_m2m', lambda o: o.some_attr),
        )
        
        expected = {
            'test_attr': 'test attr value',
            'some_field': 'test string',
            'test_fk': fk_obj.id,
            'test_m2m': ['Attribute value.'],
        }

        d = obj_to_dict(fields)(obj)
        self.assertEqual(d, expected)

    def test_with_no_fields(self):
        to_dict = obj_to_dict([])
        self.assertEqual(to_dict(object()), {})

