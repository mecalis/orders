from django.urls import path
from .views import (
    home_view,
    OrderListView,
    OrderDetailView,
    order_list_view,
    order_detail_view,
    order_new,
    queries_view,
    order_toggle_view,
    order_delete_view,
    render_pdf_view,

)

app_name = 'orders'

urlpatterns = [
    path('', home_view, name='home'),
    path('orders/', order_list_view, name='list'),

    path('orders/<pk>/', order_detail_view, name='detail'),
    path('orders-new/', order_new, name='new'),
    path('orders-queries/', queries_view, name='queries_view'),
    path('order-toggle/', order_toggle_view, name='order_toggle'),
    path('orders/<pk>/delete', order_delete_view, name='order_delete'),
    path('orders-pdf/', render_pdf_view, name='pdf'),

]