from django.db import models
from django.forms import ModelForm, CharField, Textarea
from django import forms
from appModel.models import Table, Order, Order_food, Receipt,Customer_buffet, Customer, Order_buffet

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

class Order_buffet_form(ModelForm):
    class Meta:
        model = Order_buffet
        exclude = ['order_id','order']
        widgets={
            "earnest":forms.TextInput(attrs={'class':'form-control'}),
            "location":forms.TextInput(attrs={'class':'form-control'}),
            "date": forms.DateInput(attrs={'id':'input_date','name':'date'}, format=['%d-%m-%Y']),
            "start_time": forms.TimeInput(attrs={'id':'input_starttime','name':'start_time'}, format=['%H:%M']),
            "end_time": forms.TimeInput(attrs={'id':'input_endtime','name':'end_time'}, format=['%H:%M']),
        }
        labels = {
            'earnest': 'ค่ามัดจำ',
            'location': 'สถานที่',
            'date' : 'วันที่',
            'start_time': 'เวลาเริ่ม',
            'end_time': 'เวลาสิ้นสุด',
        }

class Order_food(ModelForm):
    class Meta:
        model = Order_food
        fields = ['food', 'unit']


class Cus_buffet(ModelForm):
    class Meta:
        model = Customer_buffet
        exclude = ['customer']
        widgets={
            "company":forms.TextInput(attrs={'class':'form-control'}),
            "phone":forms.TextInput(attrs={'class':'form-control'}),
            "address":forms.Textarea(attrs={'class':'form-control'}),  
        } 
        labels = {
            'company': 'ชื่อบริษัท',
            'phone': 'เบอร์โทรศัพท์',
            'address': 'ที่อยู่',
        }


class Customer_form(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        widgets={
            "name":forms.TextInput(attrs={'class':'form-control'}),
            "amount":forms.TextInput(attrs={'class':'form-control'}),
        } 
        labels = {
            'name': 'ชื่อลูกค้า',
            'amount': 'จำนวนลูกค้า',
        }



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
