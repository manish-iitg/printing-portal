from django import forms
from .models import order

CHOICES = (
    (True, 'Black and White'),
    (False, 'Color')
)


class PlaceOrderForm(forms.Form):
    docfile = forms.FileField(
        label='Please select the PDF files', 
        help_text='Allowed file size: 10 MB', 
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )
    no_of_copies = forms.IntegerField()
    black_and_white = forms.ChoiceField(
        choices = CHOICES, 
        label="Print Type", 
        initial='', 
        widget=forms.Select(), 
    )
    class Meta:
        model = order
        fields = ['docfile', 'no_of_copies', 'black_and_white']

class OTPForm(forms.Form):
    OTP = forms.IntegerField()
