from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="staff_index"),
    path('edit_food/', views.Add_edit_food.as_view(), name="edit_food"),
    path('delete_food/<int:food_id>/', views.delete_food, name="delete_food"),
    path('edit_table/', views.Add_edit_table.as_view(), name="edit_table"),
    path('delete_table/<int:table_id>/', views.delete_table, name="delete_table")
]