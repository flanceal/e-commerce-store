from django import forms


class ReviewForm(forms.Form):
    review = forms.CharField(max_length=300)