from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from appModel.models import Order_food

# Create your views here.

@login_required
@permission_required("appModel.change_order_food")
def index(request):
    order_foods = Order_food.objects.filter(status=False).filter(order__receipt=None).filter(order__order_type='order_in')
    for order_food in order_foods:
        order_food.unit = min(order_food.unit, order_food.food.amount)
        order_food.food_price = order_food.unit*order_food.food.price
        order_food.save()
        if order_food.unit == 0:
            order_food.delete()
    context = {
        "order_foods" : Order_food.objects.filter(status=False).filter(order__receipt=None).filter(order__order_type='order_in').order_by("id"),
        #ออเดอร์อาหารของบุฟเฟ่ต์
        "order_buffets" : Order_food.objects.filter(status=False).filter(order__receipt=None).filter(order__order_type='order_buffet').order_by("id")
    }
    return render(request, "kitchen/check_order.html", context=context)

@login_required
@permission_required("appModel.change_order_food")
def accept_order_food(request, order_id):
    order_food = Order_food.objects.get(pk=order_id)
    order_food.status = True
    food = order_food.food
    food.amount -= order_food.unit
    order_food.save()
    food.save()
    return redirect('kitchen')

@login_required
@permission_required("appModel.change_order_food")
def delete_order_food(request, order_id):
    order_food = Order_food.objects.get(pk=order_id)
    order_food.delete()
    return redirect('kitchen')
