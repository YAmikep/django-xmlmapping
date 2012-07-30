# Django
from django.test import TestCase

# Third-party apps
from lxml import etree  # http://lxml.de/

# Internal
from ...utils.xmlhelper import XMLHelper

XML = """<?xml version="1.0" encoding="utf-8"?>
        <rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
            <channel>
                <item>
                    <title>Title item 1</title>
                    <media:desc>Desc item 1</media:desc>
                </item>
                <item>
                    <title>Title item 2</title>
                    <media:desc>Desc item 2</media:desc>
                </item>
                <item>
                    <title>Title item 3</title>
                    <media:desc>Desc item 3</media:desc>
                </item>
                <item>
                    <title>Title item 4</title>
                    <media:desc>Desc item 4</media:desc>
                </item>
            </channel>
        </rss>
    """
NB_ITEMS = 4
DOC = etree.fromstring(XML)
DOC_CHANNEL = DOC.getchildren()[0]


class GetElementsKnownValues(TestCase):

    def test_root_without_node_path(self):
        nb_elements = len(XMLHelper.get_elements('rss.channel.item', DOC))

        self.assertEqual(nb_elements, NB_ITEMS)

    def test_root_with_node_path(self):
        nb_elements = len(XMLHelper.get_elements('rss.channel.item', DOC, 'rss'))

        self.assertEqual(nb_elements, NB_ITEMS)

    def test_inner_element_with_node_path(self):
        nb_elements = len(XMLHelper.get_elements('rss.channel.item', DOC_CHANNEL, 'rss.channel'))

        self.assertEqual(nb_elements, NB_ITEMS)

    def test_inner_element_full_path(self):
        nb_elements = len(XMLHelper.get_elements('channel.item', DOC_CHANNEL))

        self.assertEqual(nb_elements, NB_ITEMS)

    def test_inner_element_path(self):
        nb_elements = len(XMLHelper.get_elements('item', DOC_CHANNEL))

        self.assertEqual(nb_elements, NB_ITEMS)

    def test_root_wrong_path(self):
        nb_elements = len(XMLHelper.get_elements('item', DOC))

        self.assertEqual(nb_elements, 0)

    def test_inner_element_without_node_path(self):
        nb_elements = len(XMLHelper.get_elements('rss.channel.item', DOC_CHANNEL))

        self.assertEqual(nb_elements, 0)


class GetTextKnownValues(TestCase):

    def test_text_tag_element(self):
        elems = XMLHelper.get_elements('rss.channel.item', DOC)
        value = XMLHelper.get_text(elems[1], 'title')

        self.assertEqual(value, 'Title item 2')

    def test_text_tag_element_with_ns(self):
        elems = XMLHelper.get_elements('rss.channel.item', DOC)
        value = XMLHelper.get_text(elems[2], 'media:desc')

        self.assertEqual(value, 'Desc item 3')

    def test_text_element(self):
        elems = XMLHelper.get_elements('rss.channel.item.media:desc', DOC)
        value = XMLHelper.get_text(elems[3])

        self.assertEqual(value, 'Desc item 4')


class PrefixToURIKnownValues(TestCase):
    tag = 'ns1:tag1.ns2:tag2.ns1:tag3'
    tag_backslash = 'ns1:tag1/ns2:tag2/ns1:tag3'
    ns_map = {
            'ns1': 'http://www.ns1.com',
            'ns2': 'http://www.ns2.com'
        }
    tag_uri = '{http://www.ns1.com}tag1.{http://www.ns2.com}tag2.{http://www.ns1.com}tag3'
    tag_uri_backslash = '{http://www.ns1.com}tag1/{http://www.ns2.com}tag2/{http://www.ns1.com}tag3'

    def test_uri_to_prefix_to_uri(self):

        tag_a = XMLHelper.ns_prefix_to_uri(self.tag, self.ns_map)
        self.assertEqual(tag_a, self.tag_uri)

        tag_b = XMLHelper.ns_uri_to_prefix(tag_a, self.ns_map)
        self.assertEqual(tag_b, self.tag)

    def test_uri_to_prefix_to_uri_backslash(self):

        tag_a = XMLHelper.ns_prefix_to_uri(self.tag_backslash, self.ns_map)
        self.assertEqual(tag_a, self.tag_uri_backslash)

        tag_b = XMLHelper.ns_uri_to_prefix(tag_a, self.ns_map)
        self.assertEqual(tag_b, self.tag_backslash)


class XPathKnownValues(TestCase):
    path = 'ns1:tag1.ns2:tag2.ns1:tag3'
    ns_map = {
            'ns1': 'http://www.ns1.com',
            'ns2': 'http://www.ns2.com'
        }
    xpath = '{http://www.ns1.com}tag1/{http://www.ns2.com}tag2/{http://www.ns1.com}tag3'

    def test_basic(self):

        xpath_a = XMLHelper.to_xpath(self.path, self.ns_map)
        self.assertEqual(xpath_a, self.xpath)
