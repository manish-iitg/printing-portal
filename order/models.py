from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
 
# Create your models here.
class order(models.Model):
    # customer info
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField(default='customer@iitg.ac.in')

    # shopkeeper info
    shopkeeper_email = models.EmailField(default='shopkeeper@iitg.ac.in')
    shopkeeper_location = models.CharField(max_length=100)

    # doc info(files, pages to be printed, black/white or colour, etc)
    docfile = models.FileField(upload_to = '', default = 'blank.pdf', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    starting_page = models.IntegerField(default = 1)
    ending_page = models.IntegerField(default = 1)
    no_of_copies = models.IntegerField(default = 1)
    black_and_white = models.BooleanField(required = False, default = True)

    # order details
    cost = models.IntegerField(default = 0)
    date_ordered = models.DateTimeField(default = timezone.now)
    payment_status = models.BooleanField(default = False)
    printing_status = models.BooleanField(default = False)
    payment_id = models.CharField(default = '0000000000', max_length=100)

    def __str__(self):
        return self.customer_name

