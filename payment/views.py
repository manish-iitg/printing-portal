from django.shortcuts import render
from order.models import order
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import razorpay

# Create your views here.
def gateway(request):
    if request.method == "POST":
        email = request.session['user']['email']
        order_instance = order.objects.filter(customer_email = email).last()
        cost = order_instance.cost*100
        client = razorpay.Client(auth = ("rzp_test_aBF0M5yvtP4PDr", "lPodFzCQ4YXDa9l8XfYCfgB3"))
        razorpay_order_generation = client.order.create({'amount':cost, 'currency': 'INR', 'payment_capture':'1'})
        order_instance.order_id = razorpay_order_generation['id']
        order_instance.save()
        return render(request,'payment/index.html', {'order': razorpay_order_generation})

    return render(request,'payment/index.html')

@csrf_exempt
def success(request):
    if request.method == "POST":
        body = request.POST
        for key, val in body.items():
            if key == "razorpay_order_id":
                order_id = val
                break
        user = order.objects.get(order_id = order_id)
        user.payment_status = True
        user.save()
        messages.success(request,f'Your order has been placed.')
    return render(request, 'payment/success.html')
