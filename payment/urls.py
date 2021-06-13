from django.urls import path
from . import views

urlpatterns = [
	path('pay/',views.gateway, name = 'gateway'),
    path('pay/success/',views.success, name = 'success')
]