from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="staff_index"),
    path('edit_food/', views.edit_food, name="edit_food"),
]