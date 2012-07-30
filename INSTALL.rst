Thanks for downloading django-xmlmapping.

Installation
============


Install dependencies
--------------------

The following modules are required:

* ``django-jsonfield``: http://pypi.python.org/pypi/django-jsonfield/
* ``lxml``: http://lxml.de/

As for now, it has just been tested with: Python 2.7, Django 1.4, django-jsonfield 0.8.10 and lxml 2.3.4
but feel free to try it with other versions and let me know.

You can use the file ``requirements.txt`` with pip::

    pip install -r requirements.txt
    

Install django-feedstorage
----------------------------

Run the following command inside this directory::

    python setup.py install

Or install from PyPI with ``pip``::

    pip install django-xmlmapping

Or if you'd prefer you can simply place the included ``xmlmapping``
directory somewhere on your Python path, or symlink to it from
somewhere on your Python path; this is useful if you're working from a
Mercurial checkout.


Add ``xmlmapping`` to your `INSTALLED_APPS` setting
----------------------------------------------------

Update the `INSTALLED_APPS` setting of your Django project::

    INSTALLED_APPS = (
    ...
    'xmlmapping',
    )


Sync the DB
-----------

If you are using South, run the migrations::

    ./manage.py migrate xmlmapping

Otherwise, run ``syncdb``::

    ./manage.py syncdb


Note that for now, this application has just been tested with Python 2.7 and a 
functional installation of Django 1.4. You can obtain Python
from http://www.python.org/ and Django from http://www.djangoproject.com/.
