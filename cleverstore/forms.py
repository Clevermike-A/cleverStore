from django import forms


class CheckoutForm(forms.Form):
    address = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=20)
    # Add other necessary fields
