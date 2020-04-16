from django.urls import path
from . import views

urlpatterns = [
    path('', views.orderlist, name="orderlist"),
    path('customer/', views.customer, name="customer"),
]