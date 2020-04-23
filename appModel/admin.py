from django.contrib import admin


from .models import *
from django.contrib.auth.models import Permission

# Register your models here.

def select_true(modeladmin, request, queryset):
    queryset.update(status=True)

def select_false(modeladmin, request, queryset):
    queryset.update(status=False)

def select_null(modeladmin, request, queryset):
    queryset.update(status=None)

class TableAdmin(admin.ModelAdmin):
    list_display = ["id", "status"]
    actions = [select_true, select_false]

class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "order_type"]

class OrderFoodAdmin(admin.ModelAdmin):
    actions = [select_true, select_false, select_null]

admin.site.register(Permission)

admin.site.register(Employee)

admin.site.register(Customer)

admin.site.register(Customer_buffet)

admin.site.register(Food)

admin.site.register(Table, TableAdmin)

admin.site.register(Order, OrderAdmin)

admin.site.register(Order_food, OrderFoodAdmin)

admin.site.register(Order_in)

admin.site.register(Order_buffet)

admin.site.register(Receipt)

admin.site.register(Tax_invoice)