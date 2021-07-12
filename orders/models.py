from django.db import models
from meals.models import Meal
from profiles.models import Profile
from django.utils import timezone
from .utils import generate_code
from django.shortcuts import reverse
from datetime import date
import datetime

class Position(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField(blank=True)
    created = models.DateTimeField(blank=True)
    # updated = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=120, blank=True, default='')

    def save(self, *args, **kwargs):
        self.price = self.meal.price * self.quantity
        if self.created == None:
            self.created = timezone.now()
        return super().save(*args, **kwargs)

    def get_orders_id(self):
        order_obj = self.order_set.first()
        return order_obj.id

    def __str__(self):
        return f"id: {self.id}, product: {self.meal.name}, quantity: {self.quantity}"

    def full_name(self):
        if self.comment == '':
            return f"{self.meal.name}"
        else:
            return f"{self.meal.name} - {self.comment[:20]}"

class Order(models.Model):
    transacton_id = models.CharField(max_length=16, blank=True)
    positions = models.ManyToManyField(Position)
    total_price = models.FloatField(blank=True, null=True)
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='customer')
    #footman = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, related_name='footman')
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(blank=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.customer.user} - {self.total_price}Ft"

    def get_absolute_url(self):
        return reverse('orders:detail', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('orders:order_delete', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.transacton_id == "":
            self.transacton_id = generate_code()
        if self.created == None:
            self.created = timezone.now()
        return super().save(*args, **kwargs)

    def get_positions(self):
        return self.positions.all()

    def check_day(self):
        # print(date.today())
        # print(self.created.strftime('%Y-%m-%d'))
        if str(date.today()) == str(self.created.strftime('%Y-%m-%d')):
            return True
        else:
            return False

    def get_created_day(self):
        return str(self.created.strftime('%Y-%m-%d'))



