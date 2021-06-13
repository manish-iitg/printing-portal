from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from order.models import order
from .forms import PlaceOrderForm

# Create your views here.
# quering into the database to find out the orders placed by the customers
def customer(request):
    email = request.session['user']['email']
    all_entries = order.objects.filter(customer_email = email)
    return render(request, 'order/display.html', {'all_entries' : all_entries})

# quering into the database to find out the orders reamining to be printed by the shopkeeper
def shopkeeper(request):
    email = request.session['user']['email']
    all_entries = order.objects.filter(shopkeeper_email = email, payment_status = True, printing_status = False)
    return render(request, 'order/display.html', {'all_entries' : all_entries})

def place_order(request):
    if request.method == 'POST':
        form = PlaceOrderForm(request.POST, request.FILES)
        if form.is_valid():
            name = request.session['user']['name']
            email = request.session['user']['email']

            shopkeeper_email = 'mgupta@iitg.ac.in'
            location = 'CORE-1'

            starting_page = form.cleaned_data.get('starting_page')
            ending_page = form.cleaned_data.get('ending_page')
            no_of_copies = form.cleaned_data.get('no_of_copies')
            black_and_white = form.cleaned_data.get('black_and_white')

            num_pages = ending_page-starting_page+1
            price_black_and_white = 1
            price_color = 5
            if black_and_white:
                cost = num_pages*price_black_and_white
                cost = cost*no_of_copies
            else:
                cost = num_pages*price_color
                cost = cost*no_of_copies
                
            order.objects.create(
                customer_name = name,
                customer_email = email,
                
                shopkeeper_email = shopkeeper_email,
                shopkeeper_location = location,

                docfile = request.FILES['docfile'],

                starting_page = starting_page,
                ending_page = ending_page,
                no_of_copies = no_of_copies, 
                black_and_white = black_and_white, 
                cost = cost,
            )
            return HttpResponseRedirect(reverse('gateway'))
    else : 
        form = PlaceOrderForm()
        key = 'user'
        if key in request.session:
            return render(request,'order/place_order.html',{'form':form, 'user': request.session[key]}) 
        else:
            return redirect('home')


