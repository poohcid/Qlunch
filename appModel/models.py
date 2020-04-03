from django.db import models

# ข้อมูลต่างๆ

class Food(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name+", "+str(self.price)