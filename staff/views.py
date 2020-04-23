import json

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from appModel.forms import (Employee_form, Food_form, TableForm,
                            User_change_form, User_form)
from appModel.models import Employee, Food, Table


@login_required
def index(request):
    return redirect('edit_food')

class Add_edit_food(View):
    food_form = Food_form()
    context = {
        "title" : "เพิ่ม/แก้ไข เมนูอาหาร",
        "edit_title" : "แก้ไขเมนูอาหาร",
        "create_title": "เพิ่มเมนูอาหาร",
    }
    template = "staff/edit_food.html"

    @method_decorator(login_required)
    @method_decorator(permission_required("appModel.change_food"))
    def get(self, request):
        self.context["form"] = self.food_form
        self.context["food"] = Food.objects.all().order_by("id")
        return render(request, self.template, context=self.context)
    
    @method_decorator(login_required)
    @method_decorator(permission_required("appModel.change_food"))
    def post(self, request):
        if request.POST.get("submit") == "create":
            food_form = Food_form(request.POST)
        else:
            food = Food.objects.get(pk=int(request.POST.get("id")))
            food_form = Food_form(request.POST, instance=food)

        if food_form.is_valid():
            food_form.save()
        return redirect('edit_food')

@csrf_exempt
@login_required
@permission_required("appModel.change_food")
def delete_food(request, food_id):
    if request.method == "DELETE":
        food = Food.objects.get(pk=food_id)
        #food.delete()
        return JsonResponse({}, status=200)

    return redirect("edit_food")


class Add_edit_table(View):
    table_form = TableForm()
    context = {
        "title" : "เพิ่ม/แก้ไข โต๊ะ",
        "edit_title" : "แก้ไขโต๊ะ",
        "create_title": "เพื่มโต๊ะ",
    }
    template = "staff/edit_table.html"

    @method_decorator(login_required)
    @method_decorator(permission_required("appModel.change_table"))
    def get(self, request):
        self.context["form"] = self.table_form
        self.context["table"] = Table.objects.all().order_by("id")
        return render(request, self.template, context=self.context)
    
    @method_decorator(login_required)
    @method_decorator(permission_required("appModel.change_table"))
    def post(self, request):
        if request.POST.get("submit") == "create":
            table_form = TableForm(request.POST)
        else:
            table = Table.objects.get(pk=int(request.POST.get("id")))
            table_form = TableForm(request.POST, instance=table)

        if table_form.is_valid():
            table_form.save()
        return redirect('edit_table')

@csrf_exempt
@login_required
@permission_required("appModel.change_table")
def delete_table(request, table_id):
    if request.method == "DELETE":
        table = Table.objects.get(pk=table_id)
        #table.delete()
        return JsonResponse({}, status=200)

    return redirect("edit_table")

@login_required
@permission_required("auth.change_user")
def edit_employee(request):
    context={}
    context["user"] = User.objects.exclude(is_superuser=True).order_by("id")
    context["title"] = "เพิ่ม/แก้ไข พนักงาน"
    return render(request, "staff/edit_employee.html", context=context)

@login_required
@permission_required("auth.change_user")
def create_employee(request):
    context={
        "user_form" : User_form(),
        "emp_form" : Employee_form(),
    }
    if request.method == "POST":
        user_form = User_form(request.POST)
        employee_form = Employee_form(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if employee_form.is_valid():
                emp = employee_form.save(commit=False)
                emp.user = user
                emp.save()
                return redirect('edit_employee')
        else:
            context["user_form"] = user_form
    return render(request, "staff/create_employee.html", context=context)

@login_required
@permission_required("auth.change_user")
def change_employee(request, user_id):
    context={}
    user = User.objects.get(pk=user_id)
    emp = Employee.objects.get(user=user)
    if request.method == "POST":
        user_form = User_change_form(request.POST, instance=user)
        employee_form = Employee_form(request.POST, instance=emp)
        if user_form.is_valid():
            user_form.save()
            if employee_form.is_valid():
                employee_form.save()
                return redirect('edit_employee')
            else:
                print(123)
        else:
            print(456)
    user_form = User_change_form(instance=user, initial={
        "role_waiter" : bool(user.groups.filter(name="waiter")),
        "role_salesman" : bool(user.groups.filter(name="salesman")),
        "role_chef" : bool(user.groups.filter(name="chef")),
        "role_staff": bool(user.groups.filter(name="staff"))
    })
    context={
        "user_form" : user_form,
        "emp_form" : Employee_form(instance=emp),
        "user_id" : user_id
    }
    return render(request, "staff/change_employee.html", context=context)

@csrf_exempt
@login_required
@permission_required("auth.change_user")
def delete_employee(request, user_id):
    if request.method == "DELETE":
        user = User.objects.get(pk=user_id)
        user.delete()
        return JsonResponse({}, status=200)
    return redirect('edit_employee')
