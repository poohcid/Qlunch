from datetime import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from appModel.models import (Customer, Customer_buffet, Order, Order_buffet,
                             Order_food, Receipt, Tax_invoice)
from appModel.forms import (Cus_buffet, Customer_form, Order_buffet_form,
                           OrderForm)


@login_required
@permission_required("appModel.add_order_buffet")
def orderlist(request):
    context = {}
    receipt = Receipt.objects.all() 
    order_receipt = []

    for i in receipt:
        order_receipt.append(i.order_id)

    context['order_receipt'] = Order_buffet.objects.filter(order_id__in=order_receipt)
    context['order_notreceipt'] = Order_buffet.objects.exclude(order_id__in=order_receipt)
    return render(request, "buffet/orderlist.html", context=context)

@login_required
@permission_required("appModel.add_order_buffet")
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

@login_required
@permission_required("appModel.add_order_buffet")
def add_order_buffet(request, cus_id):
    context = {}
    if request.method == "POST":
        order1 = Order.objects.create(
            date_book = datetime.now(),
            total_price = 0.0,
            employee = request.user,
            order_type = "order_buffet",
            customer_id= cus_id,
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
            return redirect('orderlist')
    else:
        form = OrderForm()
        form2 = Order_buffet_form()
    context['order_form'] = form
    context['buffet_form'] = form2
    context['customer'] = Customer.objects.get(pk=cus_id)
    return render(request, "buffet/add_order_buffet.html", context=context)


@login_required
@permission_required("appModel.add_tax_invoice")
def tax_invoice(request, order_id):
    context = {}
    total_price = 0
    check = [True,False]
    orderbuffet = Order_buffet.objects.get(order=order_id)
    customer = Customer_buffet.objects.get(customer_id=orderbuffet.order.customer_id)
    orderfood = Order_food.objects.filter(order_id=order_id).filter(status__in=check)
    for i in orderfood:
        total_price += i.food.price
    if total_price == 0:
        context['error'] = 'ไม่สามารถออกใบกำกับภาษีได้เนื่องจากออเดอร์นี้ไม่ได้ทำการสั่งเมนูใดเลย!'

    context['tax_invoice'] = Tax_invoice.objects.filter(order_buffet_id=orderbuffet.id)
    context['order_food'] = orderfood
    context['customer'] = customer
    context['order'] = orderbuffet
    context['total_price'] = total_price #ราคา
    context['vat'] = (total_price*7)/100 #vat
    context['total'] = total_price+(total_price*7)/100 #ราคา+vat
    context['now'] = datetime.now()

    if request.method == "POST":
        if request.POST.get('create'):
            tax = Tax_invoice.objects.create(
                date=datetime.now(),
                net_payment=total_price+(total_price*7)/100,
                name= request.POST.get('tax_name'),
                order_buffet=orderbuffet
            )
        else:
            tax = Tax_invoice.objects.get(order_buffet_id=orderbuffet.id)
            if request.POST.get('tax_name'):
                tax.name = request.POST.get('tax_name')
            tax.save()
        return render(request, "buffet/tax_invoice.html", context=context)
    return render(request, "buffet/tax_invoice.html", context=context)
