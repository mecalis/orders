from django.urls import path
from .views import my_profile_view
from .views import UserFormView


app_name = 'profiles'

urlpatterns = [
    path('', my_profile_view, name='my'),
    path('register/', UserFormView.as_view(), name='register'),

]

