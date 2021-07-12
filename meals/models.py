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
    name = models.CharField(max_length=100, help_text = "Fogás neve. Napi menü estén 'Napi menü 1' vagy 'Napi menü 2'")
    price = models.FloatField(help_text='Ára forintban')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    day = models.DateField(blank=True,default=datetime.now, help_text='Csak a napi ajánlatoknál fontos!')
    type = models.CharField(max_length=1, choices=TYPES)
    description = models.CharField(max_length=100, default = '', blank=True, help_text='Csak a napi menüknél használatos!')
    boxes = models.CharField(max_length=1, choices=BOXES, default='1', help_text='Szükséges dobozok száma')

    #
    def __str__(self):
        return str(self.name)

    def full_name(self):
        if self.description:
            return f"{self.name} - {self.description}"
        else:
            return f"{self.name}"


    def get_absolute_url(self):
        return reverse('meals:meal_update', kwargs={'pk': self.pk})

    def get_int_price(self):
        return int(self.price)

    def get_delete_url(self):
        return reverse('meals:meal_delete', kwargs={'pk': self.pk})
