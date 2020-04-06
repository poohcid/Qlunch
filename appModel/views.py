from django.shortcuts import redirect, render

# Create your views here.

def index(request):
    return redirect('work_in/')
