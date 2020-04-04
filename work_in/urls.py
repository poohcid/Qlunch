from django.urls import path
from . import views

urlpatterns = [
    path('table/', views.table, name="table"),
    path('create_table/', views.create_table, name="create_table"),

]