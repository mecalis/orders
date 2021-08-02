from django.urls import path
from .views import classifier_home_view, classifier_get_data_view, classifier_new_data_view

app_name = 'classifier'

urlpatterns = [
    path('', classifier_home_view, name='classifier-home'),
    path('get_data/', classifier_get_data_view, name='get-data'),
    path('new_data/', classifier_new_data_view, name='new-data'),
]
