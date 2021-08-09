from django.contrib import admin
from .models import Order, Position
# Register your models here.

# class PositionAdmin(admin.ModelAdmin):
#     list_display = ['meal', 'quantity']
# admin.site.register(Position, PositionAdmin)

admin.site.register(Order)
admin.site.register(Position)