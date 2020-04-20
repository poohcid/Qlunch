from django.http import HttpResponse
from django.shortcuts import render
from appModel.models import Order_food

# Create your views here.

def index(request):
    context = {
        "order_foods" : Order_food.objects.filter(status=False).order_by("id")
    }
    return render(request, "kitchen/check_order.html", context=context)
