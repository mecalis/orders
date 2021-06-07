from django.urls import path
from .views import (
    home_view,
    OrderListView,
    OrderDetailView,
    order_list_view,
    order_detail_view,
)

app_name = 'orders'

urlpatterns = [
    path('', home_view, name='home'),
    path('orders/', order_list_view, name='list'),
    path('orders/<pk>/', order_detail_view, name='detail')
]