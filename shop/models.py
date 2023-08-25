from django.db import models
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

class Category(models.Model):
    name = models.CharField(max_length=20,)

    def __str__(self):
        return self.name

class Item(models.Model):
    code = models.CharField(max_length=20,null=False)
    name = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit_price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.code} - {self.name}'

class Stock(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, primary_key=True)
    quantity = models.PositiveIntegerField()
    best_price = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.item}'

class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length = 30)
    alternative_phone = PhoneNumberField(blank=False, unique=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    def __str__(self):
        return f'{self.first_name} - {self.phone}'

class Sale(models.Model):
    CASH = 'CASH'
    MPESA = 'MPESA'
    MODE_CHOICES = [
        (CASH, 'Cash'),
        (MPESA, 'M-Pesa')
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    amount_paid = models.PositiveIntegerField()
    mode_of_payment = models.CharField(max_length=5, choices=MODE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer} {self.item} {self.quantity}'

    def clean(self):
        if self.quantity > self.item.quantity:
            raise ValidationError("You can't sell more than the items in stock")

        amount_payable = self.calculate_amount_payable()
        if self.amount_paid < amount_payable:
            raise ValidationError("Please input the correct amount for the products chosen")

    def save(self, *args, **kwargs):
        self.full_clean()
        self.item.quantity -= self.quantity
        self.item.save()
        super().save(*args, **kwargs)

    def calculate_amount_payable(self):
        return self.quantity * self.item.best_price


