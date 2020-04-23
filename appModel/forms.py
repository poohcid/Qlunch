from django.db import models
from django.forms import ModelForm, CharField, Textarea
from django import forms
from django.contrib.auth.models import User, Group
from appModel.models import Table, Order, Order_food, Receipt,Customer_buffet, Customer, Order_buffet, Food, Employee

class TableForm(ModelForm):
    class Meta:
        model = Table
        fields = "__all__"
        widgets={
            "space":forms.NumberInput(attrs={'class':'form-control', 'min':'0'}),
            "status":forms.CheckboxInput(attrs={'class':'form-control'}),
        }
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
            "detail":forms.Textarea(attrs={'class':'form-control','rows':4, 'cols':15})
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
            "location":forms.Textarea(attrs={'class':'form-control','rows':4, 'cols':15}),
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


class Food_form(ModelForm):
    class Meta:
        model = Food
        fields = "__all__"
        widgets={
            "name":forms.TextInput(attrs={'class':'form-control'}),
            "price":forms.NumberInput(attrs={'class':'form-control'}),
            "amount":forms.NumberInput(attrs={'class':'form-control'}),
        } 
        labels = {
            'name': 'ชื่อเมนูอาหาร',
            'price': 'ราคา',
            'amount': 'จำนวนที่มี',
        }

class User_form(ModelForm):
    error_messages = {
        'password_mismatch': ("กรุณากรอกรหัสผ่านให้ตรงกัน!"),
        'username_repeat' : "ชื่อผู้ใช้งานซ้ำ!"
    }
    password1 = forms.CharField(label="รหัสผ่าน", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="ยืนยันรหัสผ่าน", widget=forms.PasswordInput(attrs={'class':'form-control'}))

    #ปุ่ม
    role_waiter = forms.BooleanField(label="พนักงานบริการ", widget=forms.CheckboxInput(attrs={'class':''}), required=False)
    role_salesman = forms.BooleanField(label="พนักงานขาย", widget=forms.CheckboxInput(attrs={'class':''}), required=False)
    role_chef = forms.BooleanField(label="พ่อครัว", widget=forms.CheckboxInput(attrs={'class':''}), required=False)
    role_staff = forms.BooleanField(label="ผู้ดูแล", widget=forms.CheckboxInput(attrs={'class':''}), required=False)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]
        widgets={
            "username":forms.TextInput(attrs={'class':'form-control'}),
            "first_name":forms.TextInput(attrs={'class':'form-control'}),
            "last_name":forms.TextInput(attrs={'class':'form-control'}),
        }
        labels = {
            "username" : "ชื่อผู้ใช้งาน",
            "first_name" : "ชื่อจริง",
            "last_name" : "นามสกุล"
        }
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username):
            raise forms.ValidationError(
                self.error_messages['username_repeat'],
                code='username_repeat',
            )
        return username
    
    def save(self, commit=True):
        user = super(User_form, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if self.cleaned_data["role_waiter"]:
            user.save()
            user.groups.add(Group.objects.get(name="waiter"))
        if self.cleaned_data["role_salesman"]:
            user.save()
            user.groups.add(Group.objects.get(name="salesman"))
        if self.cleaned_data["role_chef"]:
            user.save()
            user.groups.add(Group.objects.get(name="chef"))
        if self.cleaned_data["role_staff"]:
            user.save()
            user.groups.add(Group.objects.get(name="staff"))
        if commit:
            user.save()
        return user
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    

class User_change_form(ModelForm):
    error_messages = {
        'username_repeat' : "ชื่อผู้ใช้งานซ้ำ"
    }

    #ปุ่ม
    role_waiter = forms.BooleanField(label="พนักงานบริการ", widget=forms.CheckboxInput(attrs={'class':''}), required=False)
    role_salesman = forms.BooleanField(label="พนักงานขาย", widget=forms.CheckboxInput(attrs={'class':''}), required=False)
    role_chef = forms.BooleanField(label="พ่อครัว", widget=forms.CheckboxInput(attrs={'class':''}), required=False)
    role_staff = forms.BooleanField(label="ผู้ดูแล", widget=forms.CheckboxInput(attrs={'class':''}), required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name"]
        widgets={
            "first_name":forms.TextInput(attrs={'class':'form-control'}),
            "last_name":forms.TextInput(attrs={'class':'form-control'}),
        }
        labels = {
            "first_name" : "ชื่อจริง",
            "last_name" : "นามสกุล"
        }
    
    def save(self, commit=True):
        user = super(User_change_form, self).save(commit=False)
        
        if self.cleaned_data["role_waiter"]:
            user.groups.add(Group.objects.get(name="waiter"))
        else:
            user.groups.remove(Group.objects.get(name="waiter"))
        if self.cleaned_data["role_salesman"]:
            user.groups.add(Group.objects.get(name="salesman"))
        else:
            user.groups.remove(Group.objects.get(name="salesman"))
        if self.cleaned_data["role_chef"]:
            user.groups.add(Group.objects.get(name="chef"))
        else:
            user.groups.remove(Group.objects.get(name="chef"))
        if self.cleaned_data["role_staff"]:
            user.groups.add(Group.objects.get(name="staff"))
        else:
            user.groups.remove(Group.objects.get(name="staff"))

        if commit:
            user.save()
        return user

class Employee_form(ModelForm):
    class Meta:
        model = Employee
        exclude = ['user']
        widgets={
            "phone":forms.TextInput(attrs={'class':'form-control'}),
            "address":forms.Textarea(attrs={'class':'form-control', 'rows':'3'}),
        }
        labels = {
            "phone" : "เบอร์โทรศัพท์",
            "address" : "ที่อยู่"
        }
