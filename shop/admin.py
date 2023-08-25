from django.contrib import admin
from .models import Sale, Category, Item, Stock, Customer

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('customer', 'item', 'quantity', 'amount_paid', 'mode_of_payment', 'date')
    list_filter = ('mode_of_payment', 'date')
    search_fields = ('customer__name', 'item__item__name')
    list_per_page = 20

    fieldsets = (
        ('Sale Details', {
            'fields': ('customer', 'item', 'quantity', 'amount_paid', 'mode_of_payment')
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'unit_price')
    list_filter = ('category',)
    search_fields = ('code', 'name')
    list_per_page = 20

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'best_price', 'date')
    list_filter = ('date',)
    search_fields = ('item__name',)
    list_per_page = 20

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','phone','alternative_phone')
    search_fields = ('first_name', 'phone')
    list_per_page = 20
