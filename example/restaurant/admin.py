# Django
from django.contrib import admin

# Internal
from .models import Menu, Meal, Music


class MenuAdmin(admin.ModelAdmin):
    fields = ('label',)
    list_display = ('id', 'label',)


class MealAdmin(admin.ModelAdmin):
    fields = ('title', 'price', 'about', 'nb_calories',)
    list_display = ('id', 'title', 'price', 'about', 'nb_calories',)


class MusicAdmin(admin.ModelAdmin):
    fields = ('title', 'singer', 'desc')
    list_display = ('id', 'title', 'singer', 'desc')


admin.site.register(Menu, MenuAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(Music, MusicAdmin)
