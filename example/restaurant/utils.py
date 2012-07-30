import hashlib
from lxml import etree

def md5_hash(element):
    """Make a hash of the element."""
    v = hashlib.md5()
    v.update(etree.tostring(element))
    return v.hexdigest()
