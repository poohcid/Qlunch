from django.contrib import admin


from appModel.models import *
from django.contrib.auth.models import Permission

# Register your models here.

def select_true(modeladmin, request, queryset):
    queryset.update(status=True)

def select_false(modeladmin, request, queryset):
    queryset.update(status=False)

class TableAdmin(admin.ModelAdmin):
    list_display = ["id", "status"]
    actions = [select_true, select_false]

class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "order_type"]

admin.site.register(Customer)

admin.site.register(Food)

admin.site.register(Table, TableAdmin)

admin.site.register(Order, OrderAdmin)

admin.site.register(Order_food)

admin.site.register(Order_in)

admin.site.register(Order_buffet)

admin.site.register(Receipt)

admin.site.register(Tax_invoice)
