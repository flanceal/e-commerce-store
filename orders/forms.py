from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Danil'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fartanov'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class": 'form-control', 'placeholder': 'you@example.com'}))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Ukraine, Kyiv, Kropyvnytskoho Street 27'}))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address']
