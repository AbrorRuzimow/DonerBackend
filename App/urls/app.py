from django.urls import path

from App.views.app import *
from Authenticate.views import *

app_name = 'App'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', AppLoginView.as_view(), name='login'),
    path('register/', AppRegisterView.as_view(), name='register'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddProductCart.as_view(), name='add_product_cart'),
    path('cart/remove/', RemoveProductCart.as_view(), name='remove_product_cart'),
    path('cart/delete/', DeleteProductCart.as_view(), name='delete_product_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order/history/', OrderHistoryView.as_view(), name='order_history'),
    path('order/history/<code>/', OrderView.as_view(), name='order'),
]
