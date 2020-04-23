from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="staff_index"),
    path('edit_food/', views.Add_edit_food.as_view(), name="edit_food"),
    path('delete_food/<int:food_id>/', views.delete_food, name="delete_food"),
    path('edit_table/', views.Add_edit_table.as_view(), name="edit_table"),
    path('delete_table/<int:table_id>/', views.delete_table, name="delete_table"),
    path('edit_employee/', views.edit_employee, name="edit_employee"),
    path('create_employee/', views.create_employee, name="create_employee"),
    path('edit_employee/<int:user_id>/', views.change_employee, name="change_employee")
]