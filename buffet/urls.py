from django.urls import path
from . import views

urlpatterns = [
    path('', views.orderlist, name="orderlist"),
    path('customer/', views.customer, name="customer"),
    path('add_order_buffet/<int:cus_id>/', views.add_order_buffet, name="add_order_buffet"),
    path('tax_invoice/<int:order_id>/', views.tax_invoice, name="tax_invoice"),
]