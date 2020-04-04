from django.urls import path
from . import views

urlpatterns = [
    path('', views.table, name="here_or_home"),
    path('table/', views.here_or_home , name="table"),
    path('create_table/', views.create_table, name="create_table"),
    path('at_store/', views.at_store, name="at_store"),
]