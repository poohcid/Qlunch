from django.urls import path
from . import views

urlpatterns = [
    path('', views.table, name="here_or_home"),
    #path('table/', views.here_or_home , name="table"),
    path('create_order/', views.create_order, name="create_order"),
    path('at_store/', views.at_store, name="at_store"),
]