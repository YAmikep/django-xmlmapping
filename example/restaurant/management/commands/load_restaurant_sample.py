# Django
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

# Internal
from xmlmapping.models import Mapping


class Command(BaseCommand):
    """Django command to fetch all the enabled Feeds."""
    help = 'Fetch all the enabled Feeds.'

    def handle(self, *args, **options):

        try:
            data = open('restaurant.xml').read()
            map = Mapping.objects.get(label='Restaurant Mapping')
            nb_created = map.load_xml(data)
            self.stdout.write('XML successfully loaded. %s objects created.\n' % (sum(nb_created.itervalues()),))
            self.stdout.write(' \n'.join(['%s: %s objects created' % (k, v) for (k, v) in nb_created.items()]))            
        except ObjectDoesNotExist:
            self.stderr.write('The mapping named: "Restaurant Mapping" cannot be found. Run syncdb first.')
        except:
            self.stderr.write('The mapping cannot load the file restaurant.xml.')
