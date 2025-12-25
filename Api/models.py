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
    otp_code = models.CharField(max_length=6, null=True, blank=True)
    otp_is_active = models.BooleanField(default=False)
    otp_expires = models.DateTimeField(null=True, blank=True)
    user_type = models.CharField(max_length=10, default='1')

    class Meta:
        verbose_name = "Ulanyjy"
        verbose_name_plural = "Ulanyjylar"


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
    is_active = models.BooleanField(default=False)
    cost = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Önüme bolan çykdaýjy
    price_cost = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Önümiň peýdasy
    cash_balance = models.IntegerField(default=0)  # Göterimde

    class Meta:
        verbose_name = "Önüm"
        verbose_name_plural = "Önümler"


class ProductImage(models.Model):
    product_fk = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    class Meta:
        verbose_name = "Önümiň suraty"
        verbose_name_plural = "Önümiň suratlary"


class WarehouseName(models.Model):
    name = models.CharField(max_length=500, unique=True)

    class Meta:
        verbose_name = "Serişde"
        verbose_name_plural = "Serişdeler"


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

    class Meta:
        verbose_name = "Ammardaky serişde"
        verbose_name_plural = "Ammardaky serişdeler"


class ProductWarehouse(models.Model):
    product_fk = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse_name_fk = models.ForeignKey(WarehouseName, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=3)

    class Meta:
        verbose_name = "Önüme gerek serişde"
        verbose_name_plural = "Önüme gerek bolan serişdeler"


class Cart(models.Model):
    user_pk = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sebet"
        verbose_name_plural = "Sebetler"


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

    class Meta:
        verbose_name = "Sargyt"
        verbose_name_plural = "Sargytlar"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_fk = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=500, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cash_balance = models.IntegerField(default=0)  # Göterimde

    class Meta:
        verbose_name = "Sargyt önümleri"
        verbose_name_plural = "Sargydyň önümleri"


class Payment(models.Model):
    user_fk = models.ForeignKey(Users, on_delete=models.CASCADE)
    order = models.ForeignKey(OrderItem, on_delete=models.CASCADE, null=True, blank=True)
    money = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tölegleriň taryhy"
        verbose_name_plural = "Tölegler"


class HomePicture(models.Model):
    image = models.ImageField(upload_to='home/')

    class Meta:
        verbose_name = "Reklama"
        verbose_name_plural = "Reklamalar"


class WishList(models.Model):
    user_fk = models.ForeignKey(Users, on_delete=models.CASCADE)
    product_fk = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return "{}/{}".format(self.user_fk.username, self.product_fk.name)
