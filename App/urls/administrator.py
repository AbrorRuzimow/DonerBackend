from django.urls import path

from App.views import Dashboard
from App.views.home_page import *
from App.views.order import *
from App.views.product import *
from App.views.users import *
from App.views.warehouse import *
from App.views.warehouse_name import *

app_name = 'Administrator'

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('warehouse_name/list/', WarehouseNameList.as_view(), name='warehouse_name_list'),
    path('warehouse_name/create/', WarehouseNameCreate.as_view(), name='warehouse_name_create'),
    path('warehouse_name/update/<pk>/', WarehouseNameUpdate.as_view(), name='warehouse_name_update'),
    path('warehouse_name/delete/<pk>/', WarehouseNameDelete.as_view(), name='warehouse_name_delete'),
    path('warehouse_name/multi/delete/', WarehouseNameMultiDelete.as_view(), name='warehouse_name_multi_delete'),
    path('warehouse_name/excel/download/', WarehouseNameExcelDownload.as_view(), name='warehouse_name_excel_download'),
    path('warehouse_name/excel/upload/', WarehouseNameExcelUpload.as_view(), name='warehouse_name_excel_upload'),

    path('warehouse/list/', WarehouseList.as_view(), name='warehouse_list'),
    path('warehouse/create/', WarehouseCreate.as_view(), name='warehouse_create'),
    path('warehouse/update/<pk>/', WarehouseUpdate.as_view(), name='warehouse_update'),
    path('warehouse/delete/<pk>/', WarehouseDelete.as_view(), name='warehouse_delete'),
    path('warehouse/multi/delete/', WarehouseMultiDelete.as_view(), name='warehouse_multi_delete'),
    path('warehouse/excel/download/', WarehouseExcelDownload.as_view(), name='warehouse_excel_download'),
    path('warehouse/excel/upload/', WarehouseExcelUpload.as_view(), name='warehouse_excel_upload'),

    path('product/list/', ProductList.as_view(), name='product_list'),
    path('product/create/', ProductCreate.as_view(), name='product_create'),
    path('product/update/<pk>/', ProductUpdate.as_view(), name='product_update'),
    path('product/delete/<pk>/', ProductDelete.as_view(), name='product_delete'),
    path('product/multi/delete/', ProductMultiDelete.as_view(), name='product_multi_delete'),
    path('product/warehouse/list/<pk>/', ProductWarehouseList.as_view(), name='product_warehouse_list'),
    path('product/warehouse/create/<pk>/', ProductWarehouseCreate.as_view(), name='product_warehouse_create'),
    path('product/warehouse/update/<pk>/', ProductWarehouseUpdate.as_view(), name='product_warehouse_update'),
    path('product/warehouse/delete/<pk>/', ProductWarehouseDelete.as_view(), name='product_warehouse_delete'),
    path('product/cash_back/update/<pk>/', ProductCashBackView.as_view(), name='product_cash_back'),

    path('homepage/list/', HomePageList.as_view(), name='homepage_list'),
    path('homepage/create/', HomePageCreate.as_view(), name='homepage_create'),
    path('homepage/update/<pk>/', HomePageUpdate.as_view(), name='homepage_update'),
    path('homepage/delete/<pk>/', HomePageDelete.as_view(), name='homepage_delete'),
    path('homepage/multi/delete/', HomePageMultiDelete.as_view(), name='homepage_multi_delete'),

    path('users/list/', UsersList.as_view(), name='users_list'),
    path('users/create/', UsersCreate.as_view(), name='users_create'),
    path('users/update/<pk>/', UsersUpdate.as_view(), name='users_update'),
    path('users/delete/<pk>/', UsersDelete.as_view(), name='users_delete'),
    path('users/multi/delete/', UsersMultiDelete.as_view(), name='users_multi_delete'),
    path('order/list/', OrderListView.as_view(), name='order_list'),
    path('order/<code>/', OrderDetailView.as_view(), name='order_detail_list'),
    path('order_status/register/<pk>/', OrderRegister.as_view(), name='order_register'),
    path('order_status/cancel/<pk>/', OrderCancel.as_view(), name='order_cancel'),
    path('order_status/success/<pk>/', OrderSuccess.as_view(), name='order_success'),
]
