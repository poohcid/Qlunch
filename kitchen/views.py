from django.http import HttpResponse
from django.shortcuts import render, redirect
from appModel.models import Order_food

# Create your views here.

def index(request):
    context = {
        "order_foods" : Order_food.objects.filter(status=False).order_by("id")
    }
    return render(request, "kitchen/check_order.html", context=context)

def accept_order_food(request, order_id):
    order_food = Order_food.objects.get(pk=order_id)
    order_food.status = True
    order_food.save()
    return redirect('kitchen')

def delete_order_food(request, order_id):
    order_food = Order_food.objects.get(pk=order_id)
    order_food.delete()
    return redirect('kitchen')
