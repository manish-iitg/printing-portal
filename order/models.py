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
    pdf_file = models.FileField(upload_to='foo/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    # order details
    cost = models.IntegerField(default = 0)
    date_ordered = models.DateTimeField(default = timezone.now)
    payment_status = models.BooleanField(default = False)
    printing_status = models.BooleanField(default = False)

    def __str__(self):
        return self.customer_name

