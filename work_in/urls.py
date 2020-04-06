from django.urls import path
from . import views

urlpatterns = [
    path('', views.table, name="here_or_home"),
    path('create_order/', views.create_order, name="create_order"),
    path('at_store/', views.at_store, name="at_store"),
    path('add_edit_order/<int:table_id>', views.add_edit_order, name="add_edit_order"),
]