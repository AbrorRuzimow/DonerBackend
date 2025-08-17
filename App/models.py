import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    user_type_list = (
        ('1', 'Administrator'),
        ('2', 'Manager'),
        ('3', 'User'),
    )
    wallet = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
    phone_number = models.CharField(max_length=8, unique=True, null=True, blank=True)
    user_type = models.CharField(max_length=10, null=True, blank=True, default='1')


class Product(models.Model):
    status_list = (
        ('1', 'Işjeň'),
        ('2', 'Işjeň däl')
    )
    name = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)  # Önümiň bahasy
    expensive_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Eger gymmatlasa gerek bolýar
    percentage = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=status_list, default='1')
    cost = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Önüme bolan çykdaýjy
    price_cost = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Önümiň peýdasy
    cash_balance = models.IntegerField(default=0)  # Göterimde


class ProductImage(models.Model):
    product_fk = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/')


class WarehouseName(models.Model):
    name = models.CharField(max_length=500, unique=True)


class Warehouse(models.Model):
    status_list = (
        ('1', 'Haryt bar'),
        ('2', 'Haryt gutardy'),
        ('3', 'Haryt zaýalandy'),
    )
    warehouse_name_fk = models.ForeignKey(WarehouseName, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    amount_use = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, null=True, blank=True, choices=status_list, default='1')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)


class ProductWarehouse(models.Model):
    product_fk = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse_name_fk = models.ForeignKey(WarehouseName, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=3)


class Cart(models.Model):
    user_pk = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    anonymous_user = models.CharField(max_length=250, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now=True)


def generate_unique_order_name():
    characters = string.ascii_uppercase + string.digits  # a-z A-Z 0-9
    while True:
        name = ''.join(random.choices(characters, k=8))
        if not Order.objects.filter(name=name).exists():
            return name


class Order(models.Model):
    payment_type_list = (
        ('1', 'Nagt töleg'),
        ('2', 'Nagt däl töleg'),
    )
    order_status_list = (
        ('1', 'Garaşylýar'),
        ('2', 'Tassyklandy'),
        ('3', 'Eltip berildi'),
        ('4', 'Yza gaýtaryldy'),
        ('5', 'Ýatyryldy'),
    )
    name = models.CharField(max_length=8, unique=True, editable=False, default=generate_unique_order_name)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    order_state = models.CharField(max_length=10, choices=order_status_list, default='1', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    canceled_date = models.DateTimeField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    delivery_price = models.DecimalField(max_digits=6, decimal_places=2)
    payment_type = models.CharField(max_length=10, choices=payment_type_list, null=True, blank=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_fk = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=500, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cash_balance = models.IntegerField(default=0)  # Göterimde


class Payment(models.Model):
    user_fk = models.ForeignKey(Users, on_delete=models.CASCADE)
    order = models.ForeignKey(OrderItem, on_delete=models.CASCADE, null=True, blank=True)
    money = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)


class HomePage(models.Model):
    image1 = models.FileField(upload_to='homepage/')
    image2 = models.FileField(upload_to='homepage/')
    image3 = models.FileField(upload_to='homepage/')
    image4 = models.FileField(upload_to='homepage/')
    text1 = models.TextField(max_length=100, null=True, blank=True)
    text2 = models.TextField(max_length=100, null=True, blank=True)
    text3 = models.TextField(max_length=100, null=True, blank=True)
    text4 = models.TextField(max_length=100, null=True, blank=True)
