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
    selling_price =models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.item} Quantity: {self.quantity}'

    def get_item_value(self):
        return self.item.unit_price * self.quantity

class Reorder(models.Model):
    stock = models.ForeignKey(Stock,on_delete=models.CASCADE)
    level = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.stock.item} Reorder Level: {self.level}'

class Sale(models.Model):
    CASH = 'CASH'
    MPESA = 'MPESA'
    MODE_CHOICES = [
        (CASH, 'Cash'),
        (MPESA, 'M-Pesa')
    ]

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length = 30)
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



    def save(self, *args, **kwargs):
        self.full_clean()
        self.item.quantity -= self.quantity
        self.item.save()
        super().save(*args, **kwargs)
        credit_transaction = CreditTransaction(account=Account.objects.get(name='Sales'), amount=self.amount_paid)
        credit_transaction.save()


class Expenses(models.Model):
    description=models.CharField(max_length=255,null=False)
    amount=models.PositiveIntegerField()

    def __str__(self):
        return f'{self.description} {self.amount}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Create a debit transaction for expenses
        debit_transaction = DebitTransaction(account=Account.objects.get(name='Expenses'), amount=self.amount)
        debit_transaction.save()

class Account(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class CreditTransaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)

class DebitTransaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)

