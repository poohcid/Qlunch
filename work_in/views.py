
from datetime import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render

from appModel.models import Food, Order, Order_food, Order_in, Table

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
        remove_list = order.order_food_set.exclude(food__in=request.POST.get("order_foods"))
        for order_food in remove_list:
            print(order_food)
            order_food.delete()
        for food_id in request.POST.get("order_foods"):
            food = Food.objects.get(pk=food_id)
            order_foods = order.order_food_set.filter(food=food)
            if order_foods:
                order_food = order_foods[0]
                order_food.unit = int(request.POST.get(food_id))
                order_food.food_price = int(request.POST.get(food_id))*food.price
                order_food.save()
            else:
                Order_food.objects.create(
                    food_price = int(request.POST.get(food_id))*food.price,
                    unit = int(request.POST.get(food_id)),
                    food = food,
                    order = order
                )

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
