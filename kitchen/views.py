from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from appModel.models import Order_food

# Create your views here.

@login_required
@permission_required("appModel.change_order_food")
def index(request):
    context = {
        "order_foods" : Order_food.objects.filter(status=False).filter(order__receipt=None).order_by("id")
    }
    return render(request, "kitchen/check_order.html", context=context)

@login_required
@permission_required("appModel.change_order_food")
def accept_order_food(request, order_id):
    order_food = Order_food.objects.get(pk=order_id)
    order_food.status = True
    order_food.save()
    return redirect('kitchen')

@login_required
@permission_required("appModel.change_order_food")
def delete_order_food(request, order_id):
    order_food = Order_food.objects.get(pk=order_id)
    order_food.delete()
    return redirect('kitchen')
