from django.db import models
from django.forms import ModelForm
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
        fields = "__all__"
        exclude = ['date_book']
        labels = {
            'name': 'ชื่อ ',
            'total_price': 'ราคาทั้งหมด',
            'detail': 'รายละเอียด',
            'customer': 'ลูกค้า',
            'employee': 'พนักงาน',
            'order_type': 'ชนิดของออเดอร์'

        }
