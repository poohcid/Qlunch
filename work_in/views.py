
from datetime import datetime

from django.shortcuts import redirect, render

from appModel.models import Order, Table, Order_in, Food
from .forms import OrderForm, TableForm
from django.contrib.auth.models import User

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

def add_edit_order(request, table_id):
    context = {}
    context['table'] = Table.objects.get(pk=table_id)
    context['food'] = Food.objects.all()
    return render(request, template_name='work_in/add_edit_order.html', context=context)