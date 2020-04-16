import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from appModel.models import (Customer, Food, Order, Order_food, Order_in,
                             Receipt, Table)

from .forms import OrderForm, TableForm

# Create your views here.

@login_required
def create_table(request):
    context = {}
    if request.method == "POST":
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
        #return redirect('select_table', table_id=)
    
    return redirect('here_or_home')
    

@login_required
def create_order(request):
    context = {}
    if request.method == "POST":
        order1 = Order.objects.create(
            date_book = datetime.now(),
            total_price = 0.0,
            employee = request.user,
            order_type = "order_in",
        )
        form = OrderForm(request.POST, instance=order1)
        if form.is_valid():
            order1 = form.save()
            order_in1 = Order_in.objects.create(
                order = order1
            )
            for i in request.POST.get("count_table"):
                table1 = Table.objects.get(pk=int(i))
                table1.status = True
                table1.save()
                order_in1.table.add(table1)
        else:
            order1.delete()
        return redirect('get_order', id=order1.id)

    return redirect('here_or_home')

#index work in
@login_required
def table(request):
    context = {}
    table = Table.objects.all().order_by('id')
    form_order = OrderForm()
    context['table'] = table
    context['form_order'] = form_order

    return render(request, template_name='work_in/table.html', context=context)

@login_required
def at_store(request):
    context = {}
    table = Table.objects.all().order_by('id')
    form_order = OrderForm()
    context['table'] = table
    context['form_order'] = form_order
    return render(request, template_name='work_in/at_store.html', context=context)

@login_required
@csrf_exempt
def save_order(request, order_id):
    if request.method == "POST":
        order = Order.objects.get(pk=order_id)
        food_id_list = request.POST.get("order_foods").split(",")[:-1]
        remove_list = order.order_food_set.exclude(food__in=food_id_list).filter(status=None)
        for order_food in remove_list:
            print(order_food)
            order_food.delete()
        for food_id in food_id_list:
            print(food_id)
            food = Food.objects.get(pk=food_id)
            order_foods = order.order_food_set.filter(food=food).filter(status=None)
            if order_foods:
                order_food = order_foods[0]
                order_food.unit = int(request.POST.get(food_id))
                order_food.food_price = int(request.POST.get(food_id))*food.price
                order_food.save()
            else:
                order_food = Order_food.objects.create(
                    food_price = int(request.POST.get(food_id))*food.price,
                    unit = int(request.POST.get(food_id)),
                    food = food,
                    order = order
                )
            if request.POST.get('action') == "sendorder":
                order_food.status = False
                order_food.save()
        response = {
            "status" : "บันทึกข้อมูลเรียบร้อย",
        }
        if request.POST.get('action') == "sendorder":
            response["status"] = "ส่งรายการออเดอร์เรียบร้อย"
        return JsonResponse(response, status=200)

    return redirect('here_or_home')

@login_required
def edit_order_food(request, order, table=False):
    context = {}
    context['order'] = order
    if table:
        context['table'] = table
    context['food'] = Food.objects.all()
    context['order_foods'] = order.order_food_set.all().order_by("status")
    return render(request, template_name='work_in/add_edit_order.html', context=context)
    
@login_required
def select_table(request, table_id):
    table = Table.objects.get(pk=table_id)
    order_ins = list(table.order_in_set.all())
    if not order_ins:
        return redirect('here_or_home')
    order = list(table.order_in_set.all())[-1].order
    return edit_order_food(request, order, table)

@login_required
def manage_order(request):
    context = {}   
    order_in = Order_in.objects.all()
    order_list = []
    receipt_list = []
    receipt = Receipt.objects.all()

    for r in receipt:
        receipt_list.append(r.order_id)
        
    print(receipt_list)
    for have_table in order_in:
        if not have_table.table.all():
            order_list.append(have_table.order_id)

    order_in = Order_in.objects.filter(order_id__in=order_list)
    order2 = Order.objects.filter(id__in=order_list) #order ทานที่ร้าน
    order = Order.objects.exclude(id__in=order_list) #order สั่งกลับบ้าน

    context['order2'] = order2.order_by("date_book")
    context['order'] = order.order_by("date_book")
    context['receipt'] = receipt_list
    context['all_order'] = Order.objects.all()

    return render(request, 'work_in/manage_order.html', context=context)

@login_required
def get_order(request, id):
    order = Order.objects.get(pk=id)
    return edit_order_food(request, order)

@login_required
def booking(request):
    context = {}
    context['customer'] = Customer.objects.all()
    return render(request, 'work_in/booking.html', context=context)

@login_required
def del_booking(request, id):
    customer = Customer.objects.get(pk=id)
    customer.delete()
    customer.save()
    return redirect('booking')

@login_required
def receipt(request, id):
    context = {}
    total_price = 0
    order = Order.objects.get(pk=id)
    check = [False, True]
    order_food = Order_food.objects.filter(order_id=id).filter(status__in=check)
    order_in = Order_in.objects.get(order_id=id)

    for i in order_food:  #บวกจำนวนเงินทั้งหมด
        total_price += i.food_price

    if order_in.table.all(): #เช็คว่า order นั้นมันโต๊ะหรือไม่
        table_list = []
        for i in order_in.table.all():
            table_list.append(i.id)

        context['table'] = table_list
        print(table_list)

    context['order'] = order
    context['order_food'] = order_food
    context['total_price'] = total_price #ราคา
    context['vat'] = (total_price*7)/100 #vat
    context['total'] = total_price+(total_price*7)/100 #ราคา+vat
    

    if request.method == "POST":
        new_reciept = Receipt.objects.create(
            date=datetime.now(),
            payment=total_price+(total_price*7)/100,
            detail=request.POST.get("detail"),
            order_id=order.id,
            employee_id=request.user.id
            )
        if order_in.table.all():
            for i in order_in.table.all():    
                table = Table.objects.get(pk=i.id)
                table.status = False
                table.save()
        return redirect('receipt', id)
    if total_price == 0:
        context['error'] = 'ไม่สามารถเช็คบิลได้เนื่องจากออเดอร์นี้ไม่ได้ทำการสั่งเมนูใดเลย!'
    try:  
        receipt = Receipt.objects.get(order_id=id)
        context['receipt'] = receipt
        context['emp'] = User.objects.get(pk=receipt.employee_id)
    except ObjectDoesNotExist:  
        return render(request, 'work_in/receipt.html', context=context)

    return render(request, 'work_in/receipt.html', context=context)
