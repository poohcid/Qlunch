from django.http import HttpResponse
from django.shortcuts import redirect, render
from appModel.models import Order_buffet, Order

def orderlist(request):
    context = {}
    context['order'] = Order_buffet.objects.all()
    return render(request, "buffet/orderlist.html", context=context)

def index(request):
    return HttpResponse("Hello") 

def customer(request):
    context = {}

    context['order'] = Order_buffet.objects.all()

    return render(request, "buffet/customer.html", context=context)