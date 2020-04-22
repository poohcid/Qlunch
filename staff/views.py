from django.http import HttpResponse
from django.shortcuts import redirect, render


def index(request):
    return redirect('edit_food')

def edit_food(request):
    return render(request, "staff/edit_food.html", context={})
