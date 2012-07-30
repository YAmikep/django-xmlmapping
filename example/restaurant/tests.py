# Python stdlib
import os.path

# Django
from django.test import TestCase


# Third-party apps
from lxml import etree  # http://lxml.de/

# Internal
from .models import Menu, Meal, Music
from xmlmapping.models import Mapping


XML = open(os.path.join(os.path.dirname(__file__), '../restaurant.xml')).read()
DOC = etree.fromstring(XML)


class LoadXMLTestCase(TestCase):
    def setUp(self):
        # Get the mapping
        self.map = Mapping.objects.get(label='Restaurant Mapping')

    def test_load_xml(self):

        self.map.load_xml(XML)

        self.assertEqual(Menu.objects.count(), 2)
        self.assertEqual(Meal.objects.count(), 2)
        self.assertEqual(Music.objects.count(), 3)
        self.assertEqual(Menu.objects.get(pk=2).label, u'French Toast $4.50')
        self.assertEqual(Meal.objects.get(pk=1).title, u'Belgian Waffles')
        self.assertEqual(Music.objects.get(pk=1).singer, u'Bryan Adams')
