Quick HOW-TO:
=============

Once you have well defined a mapping. You will be able to use it to load your XML data in the data base.
It will take care of creating all the objects in the data base.

    from xmlmapping.models import Mapping

    # You can find you mapping thanks to the label attribute
    map = Mapping.objects.get(label='my label')

    # Get your xml file the way you want, from a file, from an URL, etc
    # It must be a string.
    xml_data = open('myfile.xml').read()

    # Launch the mapping: it will load the data into the data base using this mapping
    map.load_xml(xml_data)

Note: XMLMapping focuses on mapping XML to models and its purpose is not to download 
any file from a URL or open a file or whatever.
Later, these features might be added to make it simpler for people having a simple 
usecase. However, in the meanwhile, as a good reusable app principle mentioned by James Benett,
one app must do one thing and do it well so I will focus on mapping for now.


Example
=======
You will find a working example project in the example folder.

Use case 
--------
Our ``restaurant`` app has 3 Models: ``Menu``, ``Meal`` and ``Music``
We want to load data into these Models from the ``restaurant.xml`` file located in the ``example`` folder.
Take a look at the XML file. Here is what we want to map:

    - all the food of the breakfast menu into the Meal and Menu Models of the django restaurant app.
    - all the CD of the jukebox catalog into the Music Model of the django restaurant app.

To see it working
-----------------
Go into the example project folder and run the following commands:

* Sync the DB (syncdb), it will automatically load the fixture that contains the sample mapping::
    
    manage.py syncdb

* Run the server::

    manage.py runserver

Check on the admin page that the mapping has been well imported from the fixture.

* Use the mapping
I made a simple management command to read the XML file and launch the mapping::

    manage.py load_restaurant_sample
    
or just type the following code in the console from the example folder::

    from xmlmapping.models import Mapping
    data = open('restaurant.xml').read() # Get the XML data
    map = Mapping.objects.get(label='Restaurant Mapping') # Get the mapping    
    report = map.load_xml(data) # Load the data using this mapping
    # The function returns a dict summarizing the number of objects created per element mapping
    print('XML loaded. %s objects created.' % (sum(report.itervalues()),))

You can check the log file (example/logs/xmlmapping.log) to have a more precise view of what happened.
Check on the admin that you now have several ``Menu``, ``Meal`` and ``Music`` objects.

  
Mapping format
==============
The mapping format is in JSON.
Let us go through the mapping from the example to explain how that works::

    {
        "restaurant.jukebox_catalog.hits:cd": {
            "models": {
                "restaurant.Music": {
                    "singer": "artist", 
                    "title": "title", 
                    "desc": ["country", "year"]
                }
            }
        }, 
        "restaurant.breakfast_menu.food": {
            "get_id": "guid",
            "models": {
                "restaurant.Menu": {
                    "label": ["gastronomy:name", "price"]
                }, 
                "restaurant.Meal": {
                    "nb_calories": "calories", 
                    "price": "price", 
                    "about": "description", 
                    "title": "gastronomy:name"
                }
            }
        }
    }
    

First of all, you must define your "element-mappings", that is to say the XML elements 
you want to map by their path (dotted path).

  {
      "restaurant.jukebox_catalog.hits:cd": {
          ...
      },
      "restaurant.breakfast_menu.food": {
          ...
      }
  }
  
Notice the use of the ``hits`` namespace for the CD element. 
Just use a colon to seperate the name of the namespace and the element.

Then define the Models you want to map for each element mapping.
You can map an element to several models. Each "element-model" mapping will
have its own configuration.

    "restaurant.breakfast_menu.food": {
        ...
        "models": {
            "restaurant.Menu": {
                ...
            }, 
            "restaurant.Meal": {
                ...
            }
        }
    }

For each "element-model" mapping, define the fields you want to map to.
A model field can be mapped to:
  - one of the inner element => "field": "tagElement"
  
    "restaurant.Meal": {
        "nb_calories": "calories", 
        "price": "price", 
        "about": "description", 
        "title": "gastronomy:name"
    }
    
Notice again the use of a ``gastronomy`` namespace for the name element.

  - several inner elements by defining a list => "field": ["tagElement1", "tagElement2"]
   the values will be joined with a space: tagElement1 tagElement2

   "restaurant.Menu": {
        "label": ["gastronomy:name", "price"]
    }, 

Again, notice that you can use namespaces.

* Identify an element

You can define how an Element can be identified by setting the ``get_id`` parameter.
It will not be tested whether it exists or not in the data base but the ID will be displayed in the log to
be able to identify which element has been mapped (or not).
Avoiding duplicates will be provided by Django itself if you set up a unique constraint on your fields.

You can use:
    - an inner element::

        "restaurant.breakfast_menu.food": {
            "get_id": "guid",
            "models": {
                ...
            }
        }

    - your own function/classmethod that will take the element as a parameter and return a value 
    (see the source code in the example (utils.py module) that calculates a MD5 hash for an element)::
        
        "restaurant.breakfast_menu.food": {
            "get_id": "restaurant.utils.md5_hash",
            "models": {
                ...
            }
        }                


Namespaces
----------
As shown in the above section, namespaces are handled. 
Just add the namespace followed by a colon in front of the tag.

  {
    "rss.channel.item": {
      "myapp.MyModel1": {
        "field1": "namespace:furtherDescription"
      }
    }
  }
