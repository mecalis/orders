from django.urls import path
from .views import (
    meal_create_view,
    meal_update_view,
    meal_list_view,
    meal_delete_view,
)

app_name = 'meals'

urlpatterns = [
    # path('', home_view, name='home'),
    path('new/', meal_create_view, name='meal_new'),
    path('<pk>/', meal_update_view, name='meal_update'),
    path('', meal_list_view, name='meal_list'),
    path('<pk>/delete/', meal_delete_view, name ='meal_delete'),
    # path('orders/', order_list_view, name='list'),
    # path('orders/<pk>/', order_detail_view, name='detail')
]