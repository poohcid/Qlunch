from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="kitchen"),
    path('accept_order_food/<int:order_id>/', views.accept_order_food, name="accept_order_food"),
    path('delete_order_food/<int:order_id>/', views.delete_order_food, name="delete_order_food"),
]