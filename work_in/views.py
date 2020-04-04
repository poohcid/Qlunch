from django.shortcuts import render, redirect
from appModel.models import Table, Order
from work_in.forms import TableForm, OrderForm
# Create your views here.
def create_table(request):
    context = {}
    if request.method == "POST":
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('table')

def create_order(request):
    context = {}
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('table')
            
def here_or_home(request):
    return render(request, template_name='work_in/here_or_home.html')

def table(request):
    context = {}
    table = Table.objects.all()
    form_order = OrderForm()
    context['table'] = table
    context['form_order'] = form_order
    
    return render(request, template_name='work_in/table.html', context=context)