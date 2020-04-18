from django.http import HttpResponse
from django.shortcuts import redirect, render
from appModel.models import Order_buffet, Order, Customer, Customer_buffet
from django.utils import timezone
from datetime import datetime
from work_in.forms import Cus_buffet, Customer_form, Order_buffet_form, OrderForm

def orderlist(request):
    context = {}
    
    context['order'] = Order_buffet.objects.all()
    return render(request, "buffet/orderlist.html", context=context)

def index(request):
    return HttpResponse("Hello") 

def customer(request):
    context = {}
    if request.method == "POST":
        form = Customer_form(request.POST)
        form2 = Cus_buffet(request.POST)
        if form.is_valid() and form2.is_valid():
            customer = form.save()
            customer_buff = form2.save(commit=False)
            customer_buff.customer = customer
            customer_buff.save()
    else:
        form = Customer_form()
        form2 = Cus_buffet()
    context['form'] = form 
    context['form2'] = form2
    context['customers'] = Customer_buffet.objects.all()
    return render(request, "buffet/customer.html", context=context)

def add_order_buffet(request, cus_id):
    context = {}
    if request.method == "POST":
        order1 = Order.objects.create(
            date_book = datetime.now(),
            total_price = 0.0,
            employee = request.user,
            order_type = "order_buffet",
        )
        form = OrderForm(request.POST, instance=order1)
        form2 = Order_buffet_form(request.POST)
        print(form.is_valid(), form2.is_valid())
        if form.is_valid() and form2.is_valid():
            print("Save")
            order = form.save()
            orderbuffet = form2.save(commit=False)

            orderbuffet.order = order
            orderbuffet.save()
    else:
        form = OrderForm()
        form2 = Order_buffet_form()
    context['order_form'] = form
    context['buffet_form'] = form2
    context['customer'] = Customer.objects.get(pk=cus_id)
    return render(request, "buffet/add_order_buffet.html", context=context)
