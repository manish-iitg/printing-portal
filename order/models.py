from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
 
# Create your models here.
class order(models.Model):
    # customer info
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField(default='customer@iitg.ac.in')
    OTP = models.IntegerField(null = True)
    
    # shopkeeper info
    shopkeeper_email = models.EmailField(default='shopkeeper@iitg.ac.in')
    shopkeeper_location = models.CharField(max_length=100)

    # doc info(files, pages to be printed, black/white or colour, etc)
    docfile = models.FileField(upload_to = '', default = 'blank.pdf')
    no_of_copies = models.IntegerField(default = 1)
    black_and_white = models.BooleanField(blank = True, default = True)

    # order details
    cost = models.IntegerField(null = True)
    date_ordered = models.DateTimeField(default = timezone.now)

    payment_status = models.BooleanField(default = False)
    printing_status = models.BooleanField(default = False)
    collected_status = models.BooleanField(default = False)

    order_id = models.CharField(max_length=50)

    def __str__(self):
        return self.customer_name

