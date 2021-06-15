from django.db import models
from django.shortcuts import reverse
from datetime import datetime

# Create your models here.

class Meal(models.Model):
    TYPES = (
        ('1', 'állandó'),
        ('2', 'napi menü'),
        ('3', 'napi táblás'),
        ('4', 'egyéb'),
    )
    BOXES = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
    )
    name = models.CharField(max_length=100)
    price = models.FloatField(help_text='Ára forintban')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    day = models.DateField(blank=True,default=datetime.now, help_text='Csak a napi ajánlatoknál fontos!')
    type = models.CharField(max_length=1, choices=TYPES)
    boxes = models.CharField(max_length=1, choices=BOXES, default='1', help_text='Szükséges dobozok száma')
    #
    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('meals:meal_update', kwargs={'pk': self.pk})

    def get_int_price(self):
        return int(self.price)

    def get_delete_url(self):
        return reverse('meals:meal_delete', kwargs={'pk': self.pk})
