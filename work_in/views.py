from django.shortcuts import render, redirect
from appModel.models import Table
from work_in.forms import TableForm
# Create your views here.
def create_table(request):
    context = {}
    if request.method == "POST":
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('table')
            
    

def table(request):
    context = {}
    table = Table.objects.all()
    form_table = TableForm()
    context['table'] = table
    context['form_table'] = form_table
    
    return render(request, template_name='work_in/table.html', context=context)