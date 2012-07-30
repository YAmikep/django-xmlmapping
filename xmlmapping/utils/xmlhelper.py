# Python stdlib
import re

# Internal
from . import html

# PATTERNS
PREFIX_PATTERN = re.compile(r'([a-zA-Z0-9_]*?:)')
URI_PATTERN = re.compile(r'({.*?})')


class ElementNotFound(Exception):
    pass

class XMLHelper(object):

    @classmethod
    def to_xpath(cls, path, nsmap):
        """Converts a dotted path to a xpath format.
        i.e. dots are replaced by backslash and prefix are replaced by URI
        
        Args:
            path: the dotted path to convert
            nsmap: the namespace mapping to use
            
        Returns:
            A string
        """
        if path is None:
            return None

        return cls.ns_prefix_to_uri(path.replace('.', '/'), nsmap)

    @staticmethod
    def ns_prefix_to_uri(path, ns_map):
        """Replaces the prefixes of a path by their URI.
        prefix:tag_name -> {uri}tag_name

        Args:
            path: the path to convert
            ns_map: Namespace prefix->URI mapping

        Returns:
            A String being the converted path.
        """

        prefixes = PREFIX_PATTERN.findall(path)
        for p in prefixes:
            path = path.replace(p, '{%s}' % (ns_map[p[:-1]],))

        return path

    @staticmethod
    def ns_uri_to_prefix(path, ns_map):
        """Replaces the URI of a path by their prefix.
        {uri}tag_name -> prefix:tag_name

        Args:
            path: the path to convert
            ns_map: Namespace prefix->URI mapping

        Returns:
            A String being the converted path
        """

        uri = URI_PATTERN.findall(path)

        # Reverse key, values
        ns_map = dict((v, k) for k, v in ns_map.iteritems())

        for u in uri:
            path = path.replace(u, '%s:' % (ns_map[u[1:-1]],))

        return path

    @classmethod
    def get_elements(cls, path, node, node_path=None):
        """Finds all the elements matching the path starting from the node.

        Args:
            path: the dotted path of the elements to seek
            node: the node from which to seek
            node_path: the path of the node. Not mandatory but needed when the path includes the parents.

        Returns:
            A list of elements
        """
        # The node is actually a "path" element
        if path == node_path:
            return [node]

        # Set the node_path if not provided
        if not node_path:
            node_path = node.tag

        # Removes the node_path from the path if it exists
        # And replaces dots
        if path.startswith(node_path):
            path = path[path.find(node_path) + len(node_path) + 1:]

        path = cls.to_xpath(path, node.nsmap)

        return node.findall(path)

    @classmethod
    def get_text(cls, element, tag=None):
        """Get the text value of the first tag found in an element or the text value of the element itself.
        
        Args:
            element: a node element
            tag: the tag to look for
            
        Returns:
            A string.
        
        Raises:
            An ElementNotFound exception when the tag cannot be found in the element.
        """
        if tag is not None:
            path = cls.to_xpath(tag, element.nsmap)
            text = element.findtext(path)
            if  text is not None:
                return text
            else:
                raise ElementNotFound('%s (path=%s) not found in the element' % (tag, path,))

        return element.text

    @classmethod
    def get_text_unescape(cls, element, tag=None):
        """Get the unescape text value of the first tag found in an element or the text value of the element itself.
        
        Args:
            element: a node element
            tag: the tag to look for
            
        Returns:
            An unescape string.
        
        Raises:
            An ElementNotFound exception when the tag cannot be found in the element.
        """
        return html.unescape(cls.get_text(element, tag))
