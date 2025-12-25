from datetime import timedelta

from django.contrib import admin
from django.db.models import Count, Sum
from django.template.response import TemplateResponse
from django.urls import path
from django.utils import timezone
from django.utils.html import format_html
from .models import (
    Users, Product, ProductImage, WarehouseName, Warehouse,
    ProductWarehouse, Cart, Order, OrderItem, Payment, HomePicture
)


# ================================
# CUSTOM USER ADMIN
# ================================
@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "otp_code", "otp_is_active", "otp_expires", "wallet", "user_type", "is_active",
                    "is_staff")
    list_filter = ("user_type", "is_staff", "is_active")
    search_fields = ("username", "email")
    readonly_fields = ("last_login", "date_joined")

    fieldsets = (
        ("User Info", {
            "fields": ("username", "password", "email", "wallet", "user_type")
        }),
        ("OTP Info", {
            "fields": ("otp_code", "otp_is_active", "otp_expires"),
            "classes": ("collapse",)
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Important dates", {
            "fields": ("last_login", "date_joined")
        })
    )


# ================================
# PRODUCT IMAGE INLINE
# ================================
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


# ================================
# PRODUCT ADMIN
# ================================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "expensive_price", "percentage", "is_active", "cash_balance")
    list_filter = ("is_active",)
    search_fields = ("name",)
    inlines = [ProductImageInline]


# ================================
# PRODUCT IMAGE
# ================================
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product_fk", "image")
    list_filter = ("product_fk",)
    search_fields = ("product_fk__name",)


# ================================
# WAREHOUSE NAME
# ================================
@admin.register(WarehouseName)
class WarehouseNameAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


# ================================
# WAREHOUSE
# ================================
@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = (
        "id", "warehouse_name_fk", "amount", "amount_use",
        "status", "price", "date"
    )
    list_filter = ("status", "warehouse_name_fk")
    search_fields = ("warehouse_name_fk__name",)
    readonly_fields = ("date",)


# ================================
# PRODUCT WAREHOUSE
# ================================
@admin.register(ProductWarehouse)
class ProductWarehouseAdmin(admin.ModelAdmin):
    list_display = ("id", "product_fk", "warehouse_name_fk", "amount")
    list_filter = ("warehouse_name_fk",)
    search_fields = ("product_fk__name", "warehouse_name_fk__name")


# ================================
# CART
# ================================
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user_pk", "product", "quantity", "date_added")
    search_fields = ("user_pk__username", "product__name")
    list_filter = ("date_added",)


# ================================
# ORDER ITEM INLINE
# ================================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


# ================================
# ORDER ADMIN
# ================================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "user", "colored_status", "date",
        "total_price", "delivery_price", "colored_payment"
    )
    list_filter = ("order_state", "payment_type", "date")
    search_fields = ("name", "user__username", "phone_number")
    readonly_fields = ("date",)
    inlines = [OrderItemInline]

    actions = ["make_approved", "make_delivered", "make_cancelled"]

    def colored_status(self, obj):
        colors = {
            '1': 'gray',  # Garaşylýar
            '2': 'blue',  # Tassyklandy
            '3': 'green',  # Eltip berildi
            '4': 'orange',  # Yza gaýtaryldy
            '5': 'red',  # Ýatyryldy
        }
        return format_html(
            '<span style="padding:4px 8px; color:white; border-radius:6px; background:{};">{}</span>',
            colors.get(obj.order_state, 'gray'),
            obj.get_order_state_display()
        )

    colored_status.short_description = "Status"

    def colored_payment(self, obj):
        colors = {
            '1': 'green',
            '2': 'blue',
        }
        return format_html(
            '<span style="padding:4px 8px; color:white; border-radius:6px; background:{};">{}</span>',
            colors.get(obj.payment_type, 'gray'),
            obj.get_payment_type_display()
        )

    colored_payment.short_description = "Payment"

    def make_approved(self, request, queryset):
        queryset.update(order_state='2')

    make_approved.short_description = "Tassykla"

    def make_delivered(self, request, queryset):
        queryset.update(order_state='3')

    make_delivered.short_description = "Eltip berildi"

    def make_cancelled(self, request, queryset):
        queryset.update(order_state='5')

    make_cancelled.short_description = "Ýatyrylansyn"


# ================================
# ORDER ITEM
# ================================
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product_fk", "name", "quantity", "price", "cash_balance")
    search_fields = ("order__name", "product_fk__name")


# ================================
# PAYMENT
# ================================
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "user_fk", "order", "money", "date")
    list_filter = ("date",)
    search_fields = ("user_fk__username",)
    readonly_fields = ("date",)


# ================================
# HOME PICTURE
# ================================
@admin.register(HomePicture)
class HomePictureAdmin(admin.ModelAdmin):
    list_display = ("id", "image")


# ================================
# ADMIN DASHBOARD - CHARTS
# ================================
def dashboard_view(request):
    # So'nggi 7 kun (shu jumladan bugun)
    today = timezone.now().date()
    days = [today - timedelta(days=i) for i in reversed(range(7))]  # oldest -> newest

    orders_daily = []
    for d in days:
        cnt = Order.objects.filter(date__date=d).count()
        orders_daily.append({"day": d.strftime("%Y-%m-%d"), "total": cnt})

    # Top 5 sotilgan productlar (OrderItem bo'yicha)
    top_products_qs = (
        OrderItem.objects
        .values("product_fk__name")
        .annotate(total=Sum("quantity"))
        .order_by("-total")[:5]
    )
    # convert queryset-like to list for template safety
    top_products = [{"name": p["product_fk__name"], "total": p["total"]} for p in top_products_qs]

    context = admin.site.each_context(request)
    context.update({
        "orders_daily": orders_daily,
        "top_products": top_products,
        "dashboard_title": "Statistikalar",
    })
    return TemplateResponse(request, "admin/dashboard.html", context)


# ---------- inject route into default admin.site ----------
# Keep original get_urls
_original_get_urls = admin.site.get_urls


def get_urls():
    urls = [
        path("dashboard/", admin.site.admin_view(dashboard_view), name="dashboard"),
    ]
    return urls + _original_get_urls()


# replace admin.site.get_urls with our wrapper
admin.site.get_urls = get_urls
