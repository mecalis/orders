from django import forms
from datetime import datetime

class OrdersSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=datetime.now)
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=datetime.now)

