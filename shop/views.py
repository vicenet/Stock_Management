from django.shortcuts import render
from django.views.generic import *
from .forms import *
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

# Create your views here.
 
class HomePageView(TemplateView):
    template_name = "shop/dashboard.html"


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
    success_url = reverse_lazy('shop:receive_stock')

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
    success_url = reverse_lazy('shop:sale_list')

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

class ReceiveStockView(FormView):
    template_name = 'shop/stock_receipt.html'
    form_class = StockReceiptForm

    def form_valid(self, form):
        item = form.cleaned_data['item']
        quantity_received = form.cleaned_data['quantity_received']
        stock = Stock.objects.get(item=item)
        stock.quantity += quantity_received
        stock.save()
        return redirect('shop:stock_list')
