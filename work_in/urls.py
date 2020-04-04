from django.urls import path
from . import views

urlpatterns = [
    path('', views.here_or_home, name="here_or_home"),
    path('table/', views.table, name="table"),
    path('create_table/', views.create_table, name="create_table"),
    

]