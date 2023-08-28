from django.contrib import admin
from .models import *

# Register the Sale model
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'item', 'quantity', 'amount_paid', 'mode_of_payment', 'date')
    list_filter = ('mode_of_payment', 'date')
    list_per_page = 20

# Register the Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register the Item model
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'unit_price')
    list_filter = ('category',)
    search_fields = ('code', 'name')
    list_per_page = 20

# Register the Stock model
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'date')
    list_filter = ('date',)
    search_fields = ('item__name',)
    list_per_page = 20

# Register the Expenses model
@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount')
    search_fields = ('description',)
    list_per_page = 20

# Register the Account model
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_per_page = 20

# Register the CreditTransaction model
@admin.register(CreditTransaction)
class CreditTransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'transaction_date')
    list_filter = ('account', 'transaction_date')
    search_fields = ('account__name',)
    list_per_page = 20

# Register the DebitTransaction model
@admin.register(DebitTransaction)
class DebitTransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'transaction_date')
    list_filter = ('account', 'transaction_date')
    search_fields = ('account__name',)
    list_per_page = 20

@admin.register(Reorder)
class Reorder(admin.ModelAdmin):
    list_display = ('stock','level')
