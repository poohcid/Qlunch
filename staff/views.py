from django.http import HttpResponse
from django.shortcuts import redirect, render
from appModel.models import Food
from work_in.forms import Food_form

def index(request):
    return redirect('edit_food')

def edit_food(request):
    context = {}
    form = Food_form()
    context["form"] = form
    context["food"] = Food.objects.all()
    return render(request, "staff/edit_food.html", context=context)

def delete_food(request, food_id):
    food = Food.objects.get(pk=food_id)
    food.delete()
    return redirect("edit_food")

