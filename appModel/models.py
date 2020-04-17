from django.db import models
from django.contrib.auth.models import User

# ข้อมูลต่างๆ

class Food(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    amount = models.IntegerField()

    def __str__(self):
        return self.name+", "+str(self.price)

class Customer(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()

    def __str__(self):
        return self.name

class Customer_buffet(models.Model):
    company = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=10)
    address = models.TextField()
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer.name

class Order(models.Model):
    name = models.CharField(max_length=255, null=True)
    date_book = models.DateTimeField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    detail = models.TextField(null=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.DO_NOTHING)
    employee = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    order_type = models.CharField(choices=(
        ("order_in", "in"),
        ("order_buffet", "buffet"),
    ), max_length=255)

class Order_food(models.Model):
    food_price = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.IntegerField()
    status = models.BooleanField(null=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.order.id)+" "+self.food.name+" "+str(self.unit)

class Receipt(models.Model):
    date = models.DateTimeField()
    payment = models.DecimalField(max_digits=8, decimal_places=2)
    detail = models.TextField(null=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)

class Table(models.Model):
    space = models.IntegerField()
    status = models.BooleanField()

class Order_in(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    table = models.ManyToManyField(Table)

class Order_buffet(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    earnest = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    location = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

class Tax_invoice(models.Model):
    date = models.DateTimeField()
    net_payment = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    name = models.CharField(max_length=255)
    order_buffet = models.OneToOneField(Order_buffet, on_delete=models.CASCADE)
