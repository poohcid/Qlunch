from django.db import models
from django.forms import ModelForm, CharField, Textarea
from django import forms
from appModel.models import Table, Order, Order_food, Receipt

class TableForm(ModelForm):
    class Meta:
        model = Table
        fields = "__all__"
        labels = {
            'space': 'ความจุ ',
            'status': 'สถานะ '
        }
        
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['name','detail']
        widgets={
            "name":forms.TextInput(attrs={'class':'form-control'}),
            "detail":forms.Textarea(attrs={'class':'form-control'})
        } 
        labels = {
            'name': 'ชื่อ ',
            'detail': 'รายละเอียด',
        }

class Order_food(ModelForm):
    class Meta:
        model = Order_food
        fields = ['food', 'unit']

# class ReceiptForm(ModelForm):
#     class Meta:
#         model = Receipt
#         fields = ['detail']
#         widgets={
#             "detail":forms.Textarea(attrs={'class':'form-control'})
#         }
#         labels = {
#             'detail': 'รายละเอียดใบเสร็จรับเงิน'
#         }
