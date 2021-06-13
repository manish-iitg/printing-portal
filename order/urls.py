from django.urls import path
from . import views as order_views

urlpatterns = [
    path('orders', order_views.customer, name='customer-orders'),
    path('orders', order_views.shopkeeper, name='shopkeeper-orders'),
]