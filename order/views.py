import os
import random
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from order.models import order
from .forms import PlaceOrderForm, OTPForm
from PyPDF2 import PdfFileMerger

# Create your views here.
# quering into the database to find out the orders placed by the customers
def customer(request):
    email = request.session['user']['email']
    all_entries = order.objects.filter(customer_email = email)
    return render(request, 'order/display.html', {'all_entries' : all_entries, 'shopkeeper_status': False})

# quering into the database to find out the orders reamining to be printed by the shopkeeper
def shopkeeper(request):
    email = request.session['user']['email']
    all_entries = order.objects.filter(shopkeeper_email = email, payment_status = True, printing_status = False)
    return render(request, 'order/display.html', {'all_entries' : all_entries, 'shopkeeper_status': True})

def place_order(request):
    if request.method == 'POST':
        form = PlaceOrderForm(request.POST, request.FILES)
        if form.is_valid():
            name = request.session['user']['name']
            email = request.session['user']['email']
            files = request.FILES.getlist('docfile')

            shop_email = 'mgupta@iitg.ac.in'
            shop_location = 'CORE-1'

            no_of_copies = form.cleaned_data.get('no_of_copies')
            black_and_white = form.cleaned_data.get('black_and_white')
            OTP = random.randint(1000, 10000)

            #creating extra pdf having name and email
            #os.chdir(settings.MEDIA_ROOT)
            #extrahash = random.randint(10000,100000)
            #fileName = str(extrahash)+ customer_email + '.pdf'
            #title = customer_name
            #subTitle = customer_email
            #pdf = canvas.Canvas(fileName)
            #pdf.setFont("Courier-Bold", 36)
            #pdf.drawCentredString(300, 590, title)
            #pdf.setFont("Courier-Bold", 24)
            #pdf.drawCentredString(290,500, subTitle)
            #pdf.save()


            # pdf merging
            merger = PdfFileMerger()
            for items in files:
                merger.append(items)
            #pdfname = random.randint(10000,100000)
            merged_file_name = email + '.pdf' #+ str(pdfname) 
            #merger.append(fileName)
            merger.write(merged_file_name)
            num_pages = len(merger.pages)
            merger.close()

            
            #calculating cost
            price_black_and_white = 1
            price_color = 5
            if black_and_white:
                cost = num_pages*price_black_and_white
            else:
                cost = num_pages*price_color
            cost = cost*no_of_copies
                
            order.objects.create(
                customer_name = name,
                customer_email = email,
                OTP = OTP,
                
                shopkeeper_email = shop_email,
                shopkeeper_location = shop_location,

                docfile = merged_file_name,
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

def download(request, path):
    file_path = path
    os.chdir(settings.MEDIA_ROOT)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    else :
        messages.warning(request,f'Document not found.')
        return redirect('home')
    
def status_change(request,path):
    transaction = order.objects.filter(payment_id = path)
    transaction.printing_status = True
    transaction.update(printing_status= True)
    print(type(transaction))
    messages.success(request,f'We will inform {transaction.last().customer_name} that documents have been printed.')
    return redirect('shopkeeper_orders')

def validator(request,path):
    form = OTPForm(request.POST)
    if form.is_valid() :
           data = form.cleaned_data
           OTP = data['OTP']
           transaction = order.objects.get(payment_id = path)
           tras = order.objects.filter(payment_id=path)
           if transaction.OTP == OTP:
                 tras.update(collected_status=True)
                 os.chdir(settings.MEDIA_ROOT)
                 if os.path.exists(transaction.docfile.name):
                    os.remove(transaction.docfile.name)
                 if os.path.exists(transaction.extra_file_name):
                    os.remove(transaction.extra_file_name)
                 messages.success(request,f'{transaction.customer_name} have collected his documents.')
                 return redirect('shopkeeper_orders')
           else :
               messages.warning(request,f'Wrong OTP entered.')
               return redirect('shopkeeper_orders')


