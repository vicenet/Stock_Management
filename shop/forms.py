from django import forms
import django_filters
from .models import *
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['code', 'name', 'category', 'unit_price']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['item', 'quantity']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),

        }


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['first_name','last_name', 'item', 'quantity', 'amount_paid','mode_of_payment']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control'}),
            'mode_of_payment': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})


class TransactionFilterForm(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='transaction_date',
        lookup_expr='gte',
        label='Start Date',
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )

    end_date = django_filters.DateFilter(
        field_name='transaction_date',
        lookup_expr='lte',
        label='End Date',
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Sale  # Use the relevant model here
        fields = []

class StockCreationForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['item', 'quantity',]
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ReorderForm(forms.ModelForm):
    class Meta:
        model = Reorder
        fields = ['stock', 'level']
        widgets = {
            'stock':forms.Select(attrs={'class':'form-control'}),
            'level':forms.NumberInput(attrs={'class':'form-control'}),
            }

class StockReceiveForm(forms.ModelForm):
    received_quantity = forms.IntegerField(label='Received Quantity', min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Stock
        fields = ['received_quantity']


class ExpensesForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ['description', 'amount']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }
