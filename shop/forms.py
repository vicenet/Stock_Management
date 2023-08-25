from django import forms
import phonenumbers
from .models import Category, Item, Stock, Customer, Sale
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber
from django.core.files.base import ContentFile
from phonenumber_field.widgets import PhoneNumberPrefixWidget
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
        fields = ['item', 'quantity', 'best_price']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'best_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }



class SaleForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100,  # Set an appropriate max length
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=_('First Name')  # Change the label to make it clear
    )
    last_name = forms.CharField(
        max_length=100,  # Set an appropriate max length
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=_('Last Name')  # Change the label to make it clear
    )
    phone = PhoneNumberField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=_('Phone Number')
    )


    class Meta:
        model = Sale
        fields = ['first_name','last_name','phone', 'item', 'quantity', 'amount_paid']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            if not phone.is_valid():
                raise forms.ValidationError('Invalid phone number')
            if phone.country_code != '254':
                raise forms.ValidationError('Phone number must belong to Kenya')
        return phone

    def clean_alternative_phone(self):
        alternative_phone = self.cleaned_data.get('alternative_phone')
        if alternative_phone:
            if not alternative_phone.is_valid():
                raise forms.ValidationError('Invalid alternative phone number')
            if alternative_phone.country_code != '254':
                raise forms.ValidationError('Alternative phone number must belong to Kenya')
        return alternative_phone

    def save(self, commit=True, *args, **kwargs):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        phone = self.cleaned_data.get('phone')

        # Check if a customer with the same name and phone number exists
        customer = Customer.objects.filter(first_name=customer_name, phone=phone).first()

        # If the customer doesn't exist, create a new one
        if not customer:
            customer = Customer(first_name=customer_name, phone=phone, alternative_phone=alternative_phone)
            customer.save()

        # Create the sale using the customer and other data
        sale = Sale(customer=customer, item=self.cleaned_data.get('item'), quantity=self.cleaned_data.get('quantity'), amount_paid=self.cleaned_data.get('amount_paid'))
        sale.save()

        return sale

class StockReceiptForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Stock.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))
    quantity_received = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
