from django.db import models

class Menu(models.Model):
    label = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s' % (
            self.label,
        )


class Meal(models.Model):
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    about = models.CharField(max_length=255)
    nb_calories = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s (%s cal - %s)' % (
            self.title,
            self.nb_calories,
            self.price
        )


class Music(models.Model):
    title = models.CharField(max_length=255)
    singer = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s - %s' % (
            self.title,
            self.singer
        )
