from django.urls import path

from App.views.manager import *

app_name = 'Manager'

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('order/list/', OrderListView.as_view(), name='order_list'),
    path('order/<code>/', OrderDetailView.as_view(), name='order_detail_list'),
    path('order_status/register/<pk>/', OrderRegister.as_view(), name='order_register'),
    path('order_status/cancel/<pk>/', OrderCancel.as_view(), name='order_cancel'),
    path('order_status/success/<pk>/', OrderSuccess.as_view(), name='order_success'),

]
