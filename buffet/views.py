from django.http import HttpResponse
from django.shortcuts import redirect, render
from appModel.models import Order_buffet, Order, Customer

from work_in.forms import Cus_buffet, Customer_form

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
            form.save()
            # form2.save(commit=False)

            # form2.customer = form
            # form2.save()
    else:
        form = Customer_form()
        form2 = Cus_buffet()
    context['form'] = form 
    context['form2'] = form2
    context['customers'] = Customer.objects.filter(order__order_type='order_buffet').distinct()
    return render(request, "buffet/customer.html", context=context)
