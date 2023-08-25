from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path


from .views import *
app_name = 'shop'

urlpatterns =[
    path('home/',HomePageView.as_view(),name = 'home'),
    path('profile/',ProfileView.as_view(), name='profile'),
    path('',LoginView.as_view(),name='loginPage'),
    path('logout/',LogoutView.as_view(),name = 'logoutPage'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('sale/<str:sale_status>/', SaleListView.as_view(), name='sales'),
    path('items/create/', ItemCreateView.as_view(), name='item_create'),
    path('items/', ItemListView.as_view(), name='item_list'),
    path('items/<int:pk>/update/', ItemUpdateView.as_view(), name='item_update'),
    path('items/<int:pk>/delete/', ItemDeleteView.as_view(), name='item_delete'),
    path('sales/create/', SaleCreateView.as_view(), name='sale_create'),
    path('sales/<int:pk>/update/', SaleUpdateView.as_view(), name='sale_update'),
    path('sales/<int:pk>/delete/', SaleDeleteView.as_view(), name='sale_delete'),
    path('stock/',StockListView.as_view(),name='stock'),
    path('receive_stock/',ReceiveStockView.as_view(), name='receive_stock'),

    ]
