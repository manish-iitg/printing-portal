import os
import random
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from order.models import order
from .forms import PlaceOrderForm, OTPForm
from reportlab.pdfgen import canvas 
from PyPDF2 import PdfFileMerger, PdfFileWriter
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

# a dict having possible shop options
shops = {
    'aagrahari@iitg.ac.in': 'Library',
    'mgupta@iitg.ac.in': 'CORE-1',
    'kevin@iitg.ac.in': 'Lohit Hostel Stationary',
}
# Create your views here.
# quering into the database to find out the orders placed by the customers
def customer(request):
    email = request.session['user']['email']
    all_entries = order.objects.filter(customer_email = email)
    return render(request, 'order/display.html', {'all_entries' : all_entries, 'shopkeeper_status': False})

# quering into the database to find out the orders reamining to be printed by the shopkeeper
def shopkeeper(request):
    form = OTPForm()
    email = request.session['user']['email']
    all_entries = order.objects.filter(shopkeeper_email = email, payment_status = True, collected_status = False)
    return render(request, 'order/display.html', {'all_entries' : all_entries, 'shopkeeper_status': True, 'form': form})

def place_order(request):
    if request.method == 'POST':
        form = PlaceOrderForm(request.POST, request.FILES)
        if form.is_valid():
            name = request.session['user']['name']
            email = request.session['user']['email']

            files = request.FILES.getlist('docfile')
            limit = 10*1024*1024

            # validation checks for file size and file type
            if len(files) > 5:
                return HttpResponse('Please select atmost 5 files at a time!')
            for file in files:
                if file.size > limit:
                    return HttpResponse('File too large. Size should not exceed 10 MB.')
                if not file.name.endswith(".pdf"):
                    return HttpResponse('File type unsupported. Please upload pdf files only.')

            # order details
            data = form.cleaned_data
            shop_email = data.get('shopkeeper_email')
            for key in shops:
                if key == shop_email:
                    shop_location = shops[key]

            no_of_copies = data.get('no_of_copies')
            black_and_white = data.get('black_and_white')
            OTP = random.randint(1000, 10000)

            
            os.chdir(settings.MEDIA_ROOT)
            #creating the pdf having name and email
            pdf = canvas.Canvas('name_email.pdf')
            pdf.setFont("Courier-Bold", 24)
            pdf.drawCentredString(300, 590, name)
            pdf.setFont("Courier-Bold", 18)
            pdf.drawCentredString(290,500, email)
            pdf.save()

            # pdf merging
            merger = PdfFileMerger()
            for file in files:
                merger.append(file)
            merger.append('name_email.pdf')
            all_entries = order.objects.filter(customer_email = email)
            merged_file_name = email + '-' + str(len(all_entries)) + '.pdf' 
            num_pages = len(merger.pages)
            merger.write(merged_file_name)
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
            return redirect('gateway')
        else:
            return HttpResponse('form enteries are invalid')
    else : 
        form = PlaceOrderForm()
        if request.session['user']:
            return render(request,'order/place_order.html',{'form': form, 'user': request.session['user']}) 
        else:
            return redirect('home')

def download(request, path):
    # file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    # if os.path.exists(file_path):

    os.chdir(settings.MEDIA_ROOT)
    if os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
            return response
    else :
        messages.warning(request,f'Document not found.')
        return redirect('shopkeeper_orders')
    
def status_change(request, path):
    print(path)
    transaction = order.objects.get(order_id = path)
    transaction.printing_status = True
    transaction.save()

    messages.success(request,f'We will inform {transaction.customer_name} that documents have been printed.')
    return redirect('shopkeeper_orders')

def OTP_validator(request,path):
    form = OTPForm(request.POST)
    if form.is_valid() :
        data = form.cleaned_data
        OTP = data['OTP']
        transaction = order.objects.get(order_id = path)
        if transaction.OTP == OTP:
            transaction.collected_status=True
            transaction.save()

            file_path = os.path.join(settings.MEDIA_ROOT, transaction.docfile.name)
            if os.path.exists(file_path):
                os.remove(file_path)
            messages.success(request, f'{transaction.customer_name} has collected his documents')
            return redirect('shopkeeper_orders')
        else :
            messages.warning(request,f'Wrong OTP entered')
            return redirect('shopkeeper_orders')
    else:
        messages.error(request,f'An error occured! Please try again')
        return redirect('shopkeeper_orders')

