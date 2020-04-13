
from datetime import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from appModel.models import Food, Order, Order_food, Order_in, Table, Customer, Receipt

from .forms import OrderForm, TableForm
# Create your views here.


def create_table(request):
    context = {}
    if request.method == "POST":
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
    
    return redirect('here_or_home')
    


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

    return redirect('here_or_home')

#index work in
def table(request):
    context = {}
    table = Table.objects.all().order_by('id')
    form_order = OrderForm()
    context['table'] = table
    context['form_order'] = form_order

    return render(request, template_name='work_in/table.html', context=context)

def at_store(request):
    context = {}
    table = Table.objects.all().order_by('id')
    form_order = OrderForm()
    context['table'] = table
    context['form_order'] = form_order
    return render(request, template_name='work_in/at_store.html', context=context)

def save_order(request, order_id):
    if request.method == "POST":
        order = Order.objects.get(pk=order_id)
        food_id_list = request.POST.get("order_foods").split(",")[:-1]
        remove_list = order.order_food_set.exclude(food__in=food_id_list).filter(status=None)
        for order_food in remove_list:
            print(order_food)
            order_food.delete()
        for food_id in food_id_list:
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

    return redirect('here_or_home')


def edit_order_food(request, order, table=False):
    context = {}
    context['order'] = order
    if table:
        context['table'] = table
    context['food'] = Food.objects.all()
    context['order_foods'] = order.order_food_set.all()
    return render(request, template_name='work_in/add_edit_order.html', context=context)
    

def select_table(request, table_id):
    table = Table.objects.get(pk=table_id)
    order_ins = list(table.order_in_set.all())
    if not order_ins:
        return redirect('here_or_home')
    order = list(table.order_in_set.all())[-1].order
    return edit_order_food(request, order, table)


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
    order2 = Order.objects.filter(id__in=order_list)
    order = Order.objects.exclude(id__in=order_list)

    context['order2'] = order2.order_by("date_book")
    context['order'] = order.order_by("date_book")
    context['receipt'] = receipt_list

    return render(request, 'work_in/manage_order.html', context=context)


def get_order(request, id):
    order = Order.objects.get(pk=id)
    return edit_order_food(request, order)


def booking(request):
    context = {}
    context['customer'] = Customer.objects.all()
    return render(request, 'work_in/booking.html', context=context)

def del_booking(request, id):
    customer = Customer.objects.get(pk=id)
    customer.delete()
    customer.save()
    return redirect('booking')


def receipt(request, id):
    context = {}
    total_price = 0
    order = Order.objects.get(pk=id)
    order_food = Order_food.objects.filter(order_id=id)
    order_in = Order_in.objects.get(order_id=id)

    for i in order_food:  #บวกจำนวนเงินทั้งหมด
        total_price += i.food_price

    if order_in.table.all(): #เช็คว่า order นั้นมันโต๊ะหรือไม่
        context['table'] = order_in.table.get().id

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
            table = Table.objects.get(pk=order_in.table.get().id)
            table.status = False
            table.save()
        new_reciept.save()
        return render(request, 'work_in/receipt.html', context=context)
    
    try:  
        receipt = Receipt.objects.get(order_id=id)
        context['receipt'] = receipt
        context['emp'] = User.objects.get(pk=receipt.employee_id)
    except ObjectDoesNotExist:  
        return render(request, 'work_in/receipt.html', context=context)


    return render(request, 'work_in/receipt.html', context=context)