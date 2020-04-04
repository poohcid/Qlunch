from django.db import models
from django.forms import ModelForm, CharField, Textarea
from django import forms
from appModel.models import Table, Order

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
         

