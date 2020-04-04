from django.contrib import admin


from appModel.models import *
from django.contrib.auth.models import Permission

# Register your models here.

admin.site.register(Customer)

admin.site.register(Food)

admin.site.register(Table)

admin.site.register(Order)

admin.site.register(Order_food)

admin.site.register(Order_in)

admin.site.register(Order_buffet)

admin.site.register(Receipt)

admin.site.register(Tax_invoice)
