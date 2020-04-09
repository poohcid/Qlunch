from django.urls import path
from . import views

urlpatterns = [
    path('', views.table, name="here_or_home"),
    path('create_order/', views.create_order, name="create_order"),
    path('at_store/', views.at_store, name="at_store"),
    path('select_table/<int:table_id>/', views.select_table, name="select_table"),
    path('save_order/<int:order_id>/', views.save_order, name="save_order"),
    path('home_order/', views.home_order, name="home_order"),
    path('order_fromhome/<int:id>', views.order_fromhome, name="order_fromhome"),
]