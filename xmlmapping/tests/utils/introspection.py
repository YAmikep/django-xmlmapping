# Django
from django.test import TestCase

# Internal
from ...utils.introspection import ModelFactory, ModelDoesNotExist


def func1(a):
    return a


class A(object):
    @classmethod
    def classmethod1(cls, a):
        return a


class SerializationDeserializationKnownValues(TestCase):

    def test_existing_model(self):
        my_label = 'my mapping'
        ins = ModelFactory.create('xmlmapping.Mapping', label=my_label)

        self.assertEqual(ins.label, my_label)

    def test_nonexisting_model(self):
        my_label = 'my mapping'

        self.assertRaises(ModelDoesNotExist, ModelFactory.create, 'wrong', label = my_label)
        self.assertRaises(ModelDoesNotExist, ModelFactory.create, 'wrong.Model', label = my_label)
