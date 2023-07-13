from django import forms


class ReviewForm(forms.Form):
    products = forms.CharField(max_length=256)
    review = forms.CharField(max_length=300)
    username = forms.CharField(max_length=100)
