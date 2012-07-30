# Python stdlib
import os.path
from importlib import import_module

# Find the path of the project package
# Resolve a single settings.py module or settings package.
_settings_module = import_module(os.environ['DJANGO_SETTINGS_MODULE'])
_project_package = import_module(_settings_module.__package__.split('.')[0])
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(_project_package.__file__)), '..'))


def get_project_root():
    return PROJECT_ROOT

    
def sum_dicts(dict1, dict2):
    
    if len(dict1) == 0:
        return dict2
    
    if len(dict2) == 0:
        return dict1

    if len(dict1) >= len(dict2):
        d = dict1
        other = dict2
    else:
        d = dict2
        other = dict1
    
    for k in d.keys():
        d[k] = d[k] + other.get(k, 0)
    
    return d