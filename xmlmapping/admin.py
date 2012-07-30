# Django
from django.contrib import admin

# Internal
from .models import Mapping


class MappingAdmin(admin.ModelAdmin):
    fields = ('label', 'data_map',)
    list_display = ('label', 'data_map',)
    search_fields = ('label',)


admin.site.register(Mapping, MappingAdmin)
