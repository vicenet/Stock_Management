from django.shortcuts import render
from itertools import chain
from django.views.generic import *
from .forms import *
from .models import *
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum

# Create your views here.
 
class HomePageView(TemplateView):
    template_name = 'shop/dashboard.html'

    def get(self, request, *args, **kwargs):
        # Get all Reorder objects
        reorder_levels = Reorder.objects.all()

        # Create a dictionary to store stock items meeting the reorder criteria
        stock_below_reorder = {}

        # Iterate through each reorder level
        for reorder_level in reorder_levels:
            stock_item = reorder_level.stock
            if stock_item.quantity <= reorder_level.level:
                # Stock item is below or equal to the reorder level
                if reorder_level.level not in stock_below_reorder:
                    stock_below_reorder[reorder_level.level] = [stock_item]
                else:
                    stock_below_reorder[reorder_level.level].append(stock_item)

        stocks = Stock.objects.all()

    # Calculate the total stock valuation
        total_valuation = sum(stock.get_item_value() for stock in stocks)
        sales = Sale.objects.all()
        total_revenue = sum(sale.amount_paid for sale in sales)

        # Calculate Total Expenses
        expenses = Expenses.objects.all()
        total_expenses = sum(expense.amount for expense in expenses)

        context = {
            'stock_below_reorder': stock_below_reorder,
            'total_valuation': total_valuation,
            'total_revenue':total_revenue,
            'total_expenses':total_expenses,
        }

        return render(self.request, self.template_name, context)

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'shop/profiles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class LoginView(View):
    template_name = 'shop/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect('/admin/')  # Redirect to the admin site
                else:
                    login(request, user)
                    return redirect('shop:home')  # Replace 'home' with the desired URL after successful login
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please provide a username and password.')

        return render(request, self.template_name)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('shop:loginPage')


class ChangePasswordView(View):
    template_name = 'shop/change_password.html'
    form_class = PasswordChangeForm

    def get(self, request):
        form = self.form_class(user=request.user)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
        return render(request, self.template_name, {'form': form})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'shop/password_reset_form.html'
    success_url = reverse_lazy('shop:password_reset_done')
    email_template_name = 'shop/password_reset_email.html'  # You can customize the email template
    subject_template_name = 'password_reset_subject.txt'  # You can customize the subject of the email

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for field_name, field in context['form'].fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        return context

    def get(self, request, *args, **kwargs):
        print("CustomPasswordResetView - GET method")
        return super().get(request, *args, **kwargs)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'shop/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'shop/password_reset_confirm.html'
    success_url = reverse_lazy('shop:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'shop/password_reset_complete.html'


# Item views
class CategoryListView(ListView):
    model = Category
    template_name = 'shop/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'shop/category_create.html'
    success_url = reverse_lazy('shop:item_create')

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'shop/category_update.html'
    success_url = reverse_lazy('shop:category_list')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'shop/category_confirm_delete.html'
    success_url = reverse_lazy('shop:item_create')

# Item views
class ItemListView(ListView):
    model = Item
    template_name = 'shop/item_list.html'
    context_object_name = 'items'


class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'shop/item_create.html'
    success_url = reverse_lazy('shop:stock_create')

    def form_valid(self, form):
        # Save the item
        self.object = form.save()

        # Store the new_item_id in the session
        self.request.session['new_item_id'] = self.object.pk

        # Redirect to the stock creation view with the item_id as an argument
        return redirect('shop:stock_create', item_id=self.object.pk)

class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'shop/item_update.html'
    success_url = reverse_lazy('shop:item_list')

class ItemDeleteView(DeleteView):
    model = Item
    template_name = 'shop/item_confirm_delete.html'
    success_url = reverse_lazy('item_list')

class SaleListView(LoginRequiredMixin, View):
    def get(self, request,sale_status):
        if sale_status == 'all':
            sales = Sale.objects.all()
        elif sale_status == 'mpesa':
            sales = Sale.objects.filter(mode_of_payment='MPESA')
        elif sale_status == 'cash':
            sales = Sale.objects.filter(mode_of_payment='CASH' )

        context = {
            'sales': sales,
            'sale_status':sale_status,
        }
        return render(request, 'shop/sale_list.html', context)


class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'shop/sales_create.html'
    def get_success_url(self):
        sale_status = self.kwargs.get('sale_status')
        return reverse_lazy('shop:sales', kwargs={'sale_status':'all'})


class SaleUpdateView(UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'shop/sale_update.html'
    success_url = reverse_lazy('shop:sale_list')

class SaleDeleteView(DeleteView):
    model = Sale
    template_name = 'shop/sale_confirm_delete.html'
    success_url = reverse_lazy('sale_list')

class StockListView(ListView):
    model = Stock
    template_name = 'shop/stock_list.html'
    context_object_name = 'stocks'


class StockCreateView(CreateView):
    model = Stock
    form_class = StockCreationForm
    template_name = 'shop/stock_create.html'  # Replace with your template name
    success_url = reverse_lazy('shop:stock')  # Replace with your desired success URL

    def get_initial(self):
        # Get the newly created item (assuming it's stored in the session)
        new_item_id = self.request.session.get('new_item_id')
        item = get_object_or_404(Item, pk=new_item_id)

        # Pre-fill the item field in the form
        return {'item': item}

    def form_valid(self, form):
        # Save the stock
        self.object = form.save()
        return super().form_valid(form)


class StockReceiveView(UpdateView):
    model = Stock
    form_class = StockReceiveForm
    template_name = 'shop/stock_receive.html'  # Replace with your template name
    success_url = reverse_lazy( 'shop:stock')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stock_name'] = self.object.item.name
        return context

    def form_valid(self, form):
        # Update the stock quantity based on the received quantity
        stock = form.instance
        received_quantity = form.cleaned_data['received_quantity']
        stock.quantity += received_quantity
        stock.save()
        return super().form_valid(form)



class IncomeStatementView(FilterView):
    template_name = 'shop/income_statement.html'
    filterset_class = TransactionFilterForm

    def get_queryset(self):
        queryset = Sale.objects.all()  # You can use Expenses if needed
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filter the queryset based on the request GET parameters
        queryset = self.get_queryset()
        filtered_data = self.filterset_class(self.request.GET, queryset=queryset).qs

        # Calculate total sales revenue
        total_sales = filtered_data.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

        # Calculate total expenses
        # Corrected total_expenses calculation
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date and end_date:
            total_expenses = Expenses.objects.filter(transaction_date__range=(start_date, end_date)).aggregate(Sum('amount'))['amount__sum'] or 0
        else:
            total_expenses = 0

        # Calculate net income
        net_income = total_sales - total_expenses

        context['total_sales'] = total_sales
        context['total_expenses'] = total_expenses
        context['net_income'] = net_income
        return context

class CreateExpensesView(View):
    template_name = 'shop/expense_form.html'

    def get(self, request):
        form = ExpensesForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ExpensesForm(request.POST)
        if form.is_valid():
            # Save the Expenses object
            expenses = form.save()

            # Create a debit transaction for expenses
            debit_transaction = DebitTransaction(account=Account.objects.get(name='Expenses'), amount=expenses.amount)
            debit_transaction.save()

            # Redirect to a success page or take further actions
            return redirect('shop:income_statement')  # Replace 'success_page' with the actual URL name for the success page

        return render(request, self.template_name, {'form': form})

class TotalsView(TemplateView):
    template_name = 'shop/totals.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate sales total
        sales_total = Sale.objects.aggregate(total=models.Sum('amount_paid'))['total'] or 0

        # Calculate expenses total
        expenses_total = Expenses.objects.aggregate(total=models.Sum('amount'))['total'] or 0

        # Get account transactions
        credit_transactions = CreditTransaction.objects.all()
        debit_transactions = DebitTransaction.objects.all()
        account_transactions = list(chain(credit_transactions, debit_transactions))
        account_transactions.sort(key=lambda x: x.transaction_date, reverse=True)

        context['sales_total'] = sales_total
        context['expenses_total'] = expenses_total
        context['account_transactions'] = account_transactions

        return context


def toggle_admin_site(request):
    if request.user.is_authenticated and request.user.is_staff:
        # If the user is authenticated and is a staff member (admin)
        return redirect('/admin/')  # Redirect to the admin site
    else:
        return redirect('/')  # Redirect to the normal site
