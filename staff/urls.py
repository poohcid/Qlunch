from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="staff_index"),
    path('edit_food/', views.edit_food, name="edit_food"),
    path('delete_food/<int:food_id>', views.delete_food, name="delete_food"),
]