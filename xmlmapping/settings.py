# Python stdlib
import os.path
import logging

# Django
from django.conf import settings as django_settings

# Internal
from .utils import PROJECT_ROOT


DEFAULT_SETTINGS = {
    # Logging settings
    'LOGGER_NAME': 'xmlmapping',
    'LOGGER_FORMAT': '%(asctime)s %(levelname)s %(message)s',
    'LOG_FILE': os.path.join(PROJECT_ROOT, 'logs/xmlmapping.log'),
    # Maximum size of one log file: when the size is reached, the file is archived and a new file is created.
    'LOG_SIZE': 5 * 1024 * 2 ** 10,  # 5 MB
    'LOG_LEVEL': logging.INFO,
}

# Get the user settings to update the default settings.
user_settings = getattr(django_settings, 'XML_MAPPING_SETTINGS', {})
XML_MAPPING_SETTINGS = dict(DEFAULT_SETTINGS.items() + user_settings.items())

globals().update(XML_MAPPING_SETTINGS)
