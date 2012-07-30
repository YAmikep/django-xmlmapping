==================
django-xmlmapping
==================

Library to map XML data to a Django data model, and persist the data in the data base.
Supports any data base supported by Django itself.

It has 2 dependencies: ``django-jsonfield`` and ``lxml``.

For now, it has just been tested with: Python 2.7, Django 1.4, django-jsonfield 0.8.10 and lxml 2.3.4
but feel free to try it with other versions and let me know.

For installation instructions, see the file ``INSTALL.rst`` in this
directory; for instructions on how to use this application, and on
what it provides, see the file ``overview.rst`` in the ``docs/``
directory.

  
  
Next things to do
-----------------

See the roadmap on Trello: https://trello.com/b/NwQGznbA

* write tests cases
* write more documentation
* test with older versions of python and django
* handle XML attributes
* handle Booleans, numbers, ...
* handle date parsing
* handle more feed formats
* make it possible to download a file right in the app
* handle mapping of nested models
* create advanced transformers
