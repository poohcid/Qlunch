from django.urls import path
from . import views

urlpatterns = [
    path('', views.table, name="here_or_home"),
    path('create_order/', views.create_order, name="create_order"),
    path('at_store/', views.at_store, name="at_store"),
    path('select_table/<int:table_id>/', views.select_table, name="select_table"),
    path('save_order/<int:order_id>/', views.save_order, name="save_order"),
    path('manage_order/', views.manage_order, name="manage_order"),
    path('get_order/<int:id>', views.get_order, name="get_order"),
]