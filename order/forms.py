from django import forms
from .models import order


CHOICES = (
    (True, 'Black and White'),
    (False, 'Color')
)

shop_CHOICES = ( 
    ('mgupta@iitg.ac.in', 'CORE-1'),
    ('aagrahari@iitg.ac.in', 'Library'),
    ('manish21082000@iitg.ac.in', 'Lohit Hostel Stationary'),
)

class PlaceOrderForm(forms.Form):
    docfile = forms.FileField(
        label='Please select the PDF files', 
        help_text='Allowed size per pdf: 10 MB', 
        widget=forms.FileInput(attrs={'multiple': True}),
    )
    no_of_copies = forms.IntegerField()
    black_and_white = forms.ChoiceField(
        choices = CHOICES, 
        label="Print Type", 
        initial='', 
        widget=forms.Select(), 
    )
    shopkeeper_email = forms.ChoiceField(
        choices = shop_CHOICES, 
        label="Choose the location you want your files to be printed from", 
        initial='', 
        widget=forms.Select(), 
    )
    class Meta:
        model = order
        fields = ['docfile', 'no_of_copies', 'black_and_white', 'shopkeeper_email']

class OTPForm(forms.Form):
    OTP = forms.IntegerField()
