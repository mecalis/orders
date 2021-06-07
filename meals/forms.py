from django import forms
from .models import Meal

class MealModelForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name', 'price','type', 'boxes']