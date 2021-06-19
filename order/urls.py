from django.urls import path
from django.conf.urls import url
from . import views as order_views

urlpatterns = [
    path('customer_orders', order_views.customer, name='customer_orders'),
    path('orders', order_views.shopkeeper, name='shopkeeper_orders'),
    path('place_order', order_views.place_order, name = 'place_order'), 
    url(r'^download/(?P<path>.*)$',order_views.download, name = 'download'),
    url(r'^change/(?P<path>.*)$',order_views.status_change,name = 'change'),
    url(r'^valid/(?P<path>.*)$',order_views.validator,name = 'valid'),
]
