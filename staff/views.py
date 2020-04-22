import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from appModel.forms import Food_form, TableForm
from appModel.models import Food, Table


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

    def get(self, request):
        self.context["form"] = self.food_form
        self.context["food"] = Food.objects.all().order_by("id")
        return render(request, self.template, context=self.context)
    
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

    def get(self, request):
        self.context["form"] = self.table_form
        self.context["table"] = Table.objects.all().order_by("id")
        return render(request, self.template, context=self.context)
    
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
def delete_table(request, table_id):
    if request.method == "DELETE":
        table = Table.objects.get(pk=table_id)
        #table.delete()
        return JsonResponse({}, status=200)

    return redirect("edit_table")
