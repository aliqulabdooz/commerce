from django.forms import ModelForm
from django import forms
from .models import Product, Comment


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('author', 'status')


class BidForm(forms.Form):
    starting_bid = forms.IntegerField(min_value=1)


class AddCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ('author', 'product', 'date_created', 'date_modified',)


