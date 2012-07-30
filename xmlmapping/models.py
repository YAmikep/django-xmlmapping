# Django
from django.db import models

# Third-party apps
import jsonfield  # http://pypi.python.org/pypi/django-jsonfield/
from lxml import etree  # http://lxml.de/

# Internal
from .log import default_logger as logger
from .utils.introspection import ModelFactory
from .utils.serializers import deserialize_function
from .utils.xmlhelper import XMLHelper
from .utils import sum_dicts

class Mapping(models.Model):
    """A mapping configuration."""
    data_map = jsonfield.JSONField(default='{}')  # need a default value
    label = models.CharField(max_length=255, unique=True)  # label for reference

    def __unicode__(self):
        return u'%s' % (
            self.label,
        )

    @property
    def log_desc(self):
        return u'<Mapping: %s>' % (self,)

    def load_xml(self, xml, root_path=None):
        """Loads a piece of XML in the DB, i.e. map XML data to a Django Model.

        Args:
            xml: a string being the XML data to load
            root_path: the root (dotted path) of the XML data. Not mandatory but needed when the XML is not the root as defined in the mapping.
                e.g. If you defined a mapping for rss.channel.item
                and the XML you are passing actually starts with the channel element, you must then set root_path to rss.channel

        Returns:
            A dict summarizing the number of objects created per element-mapping.
            #The number of created Models per "element-mapping"
        """
        log_desc = '%s - Loading XML' % (self.log_desc,)

        try:
            # Parse the XML
            root = etree.fromstring(xml, parser=etree.XMLParser())
        except Exception as e:
            logger.error('%s => XML cannot be parsed. [KO]\n%s' % (log_desc, e))
            return 0

        nb_created = {k: 0 for k in self.data_map.keys()}
        # For each element-mapping
        for e_path, conf in self.data_map.iteritems():
            nb_created[e_path] = nb_created[e_path] + self._map_elements_by_path(e_path, conf, root, root_path)

        logger.info('%s => %s' % (log_desc, ' ; '.join(['%s: %s objects created' % (k, v) for (k, v) in nb_created.items()])))

        return nb_created

    def load_xml_chunks(self, xml_chunks, root_path):
        """Loads a collection of XML chunks being all of the same kind.

        Args:
            xml_chunks: a list of XML string data to load
            root_path: the root (dotted path) of the XML data. Not mandatory but needed when the XML is not the root as defined in the mapping.
                e.g. If you defined a mapping for rss.channel.item
                and the XML you are passing actually starts with the channel element, you must then set root_path to rss.channel

        Returns:
            A dict summarizing the number of objects created per element-mapping.
            #The number of created Models per "element-mapping"

        TODO: Make it more efficient instead of a simple loop.
        """
        log_desc = '%s - Loading XML chunks' % (self.log_desc,)
        logger.info('%s => start' % (log_desc,))

        nb_created = {}
        for xml in xml_chunks:
            nb_created = sum_dicts(nb_created, self.load_xml(xml, root_path))

        logger.info('%s => end' % (log_desc,))

        return nb_created

    def _map_elements_by_path(self, path, conf, node, node_path):
        """Maps all the elements matching the path in the node with the mapping configuration.

        Args:
            path: the path of the elements to seek
            conf: the mapping configuration
            node: the node from which to seek
            node_path: the path of the node

        Returns:
            The number of Models created in the DB for all the found elements.
        """
        # Get the configuration
        get_id = conf.get('get_id', None)
        models = conf.get('models', None)
        if models is None:
            logger.error('%s => No models found in the configuration. [KO]\nconfiguration=%s' % (log_desc, conf))
            return 0

        log_desc = '%s - Mapping all the elements matching path=%s to %s Models' % (self.log_desc, path, len(models))

        # Get all the matching elements
        elems = XMLHelper.get_elements(path, node, node_path)

        # Log if no elements were found.
        if not elems:
            logger.warning('%s => No elements found. node_path=%s' % (log_desc, node_path))
            return 0

        nb_created = 0
        for elem in elems:
            nb_created = nb_created + self._map_element(elem, models, get_id)

        nb_elems = len(elems)
        nb_targeted = nb_elems * len(models)
        logger.info('%s => Found: %s, Targeted Objects: %s, Created Objects: %s %s' % (
                log_desc,
                nb_elems,
                nb_targeted,
                nb_created,
                (nb_targeted == nb_created and ['[OK]'] or ['=> numbers different [KO]'])[0]
            )
        )

        return nb_created

    def _map_element(self, element, models, get_id=None):
        """Maps an element to several models.

        Args:
            element: an XML element
            models: the models to mapped
            get_id: the function to use to calculate the ID of the element to identify it amongst the other.

        Returns:
            The number of Models created in the DB for the passed element.
        """
        elem_id = '(id:%s) ' % (self._resolve_get_id(get_id)(element),)

        status = {k: '[KO]' for k in models.keys()}
        nb_created = 0
        for app_model, fields in models.iteritems():
            try:
                ins = self._map_to_model(element, app_model, fields)
                status[app_model] = 'pk=%s' % (ins.pk)
                nb_created = nb_created + 1
                logger.info('%s - Mapping the element %sto the Model %s with fields %s => object created, pk=%s [0K]' % (
                        self.log_desc,
                        elem_id,
                        app_model,
                        fields,
                        ins.pk,
                    )
                )
            except Exception as err:
                logger.error('%s - Mapping the element %sto the Model %s with fields %s => Cannot be mapped. [K0]\n%s' % (
                        self.log_desc,
                        elem_id,
                        app_model,
                        fields,
                        err,
                    )
                )

        logger.info('%s - Element %smapped to %s Models => %s' % (
                self.log_desc,
                elem_id,
                len(models),
                ' ; '.join(['%s: %s' % (k, v) for (k, v) in status.items()]),
            )
        )

        return nb_created

    def _map_to_model(self, element, app_model, fields):
        """Maps an element to a Model.

        Args:
            element: the XML element to map
            app_model: the model to map defined by: app_label.model_name
            fields: the fields mapping

        Returns:
            The instance of the created Model.
        """
        ins = ModelFactory.create(app_model)
        self._map_to_fields(element, ins, fields)
        ins.save()
        return ins

    def _map_to_fields(self, element, ins, fields):
        """Maps an element to the fields.

        Args:
            element: the XML element to map
            ins: the instance of the created Model
            fields: the fields mapping
        """
        for field, configuration in fields.items():
            if isinstance(configuration, basestring):
                setattr(ins, field, XMLHelper.get_text_unescape(element, configuration))

            elif isinstance(configuration, list):
                values = (XMLHelper.get_text_unescape(element, v) for v in configuration)
                setattr(ins, field, ' '.join(values))

            elif isinstance(configuration, dict):
                pass  # TODO: handles advanced transformers

    def _resolve_get_id(self, get_id):
        """Resolves which function should be used to calculate the ID of an element.

        Args:
            get_id: a function/method or a string to use an inner element.

        Returns:
            A function that will take an element and returns an ID.
        """
        # Try to deserialize it
        try:
            return deserialize_function(get_id)
        except:
            pass

        # Deserialization could not figure it out
        # so let's assume it is a tag and we want to use the text of the element
        if isinstance(get_id, basestring):
            return lambda x: XMLHelper.get_text(x, get_id)

        # Nothing works, returns the get_id
        return lambda x: get_id
