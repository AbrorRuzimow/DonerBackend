from django.db.models import OuterRef, Subquery, F, Value, Case, When
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, ListView

from App.models import HomePage, Product, ProductImage, Cart, Order, OrderItem


class HomeView(TemplateView):
    template_name = 'app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        image_subquery = ProductImage.objects.filter(product_fk=OuterRef('pk')).values('image')[:1]
        context['home_models'] = HomePage.objects.all()
        context['product_list'] = Product.objects.all()[:4].annotate(image=Subquery(image_subquery))
        if self.request.user.is_authenticated:
            context['cart_count'] = Cart.objects.filter(user_pk=self.request.user).count()
        else:
            context['cart_count'] = Cart.objects.filter(anonymous_user=self.request.COOKIES.get('csrftoken')).count()
        return context


class AddProductCart(View):
    @staticmethod
    def post(request):
        data = request.POST
        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user_pk=request.user, product__id=data['product'])
                cart.quantity += 1
                cart.save()
            except Exception as e:
                print(e)
                cart = Cart()
                cart.user_pk = request.user
                cart.product_id = data['product']
                cart.quantity = 1
                cart.save()
        else:
            try:
                cart = Cart.objects.get(anonymous_user=request.COOKIES.get('csrftoken'), product__id=data['product'])
                cart.quantity += 1
                cart.save()
            except Exception as e:
                print(e)
                cart = Cart()
                cart.anonymous_user = request.COOKIES.get('csrftoken')
                cart.product_id = data['product']
                cart.quantity = 1
                cart.save()
        return JsonResponse({'message': 'success'}, status=200)


class RemoveProductCart(View):
    @staticmethod
    def post(request):
        data = request.POST
        if request.user.is_authenticated:
            cart = Cart.objects.get(user_pk=request.user, product__id=data['product'])
            if cart.quantity == 1:
                cart.delete()
            else:
                cart.quantity -= 1
                cart.save()
        else:
            cart = Cart.objects.get(anonymous_user=request.COOKIES.get('csrftoken'), product__id=data['product'])
            if cart.quantity == 1:
                cart.delete()
            else:
                cart.quantity -= 1
                cart.save()
        return JsonResponse({'message': 'success'}, status=200)


class DeleteProductCart(View):
    @staticmethod
    def post(request):
        data = request.POST
        if request.user.is_authenticated:
            cart = Cart.objects.get(user_pk=request.user, product__id=data['product'])
            cart.delete()
        else:
            cart = Cart.objects.get(anonymous_user=request.COOKIES.get('csrftoken'), product__id=data['product'])
            cart.delete()
        return JsonResponse({'message': 'success'}, status=200)


class CartView(TemplateView):
    template_name = 'app/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        image_subquery = ProductImage.objects.filter(product_fk=OuterRef('product')).values('image')[:1]
        total_subquery = str(OuterRef('pk'))
        if self.request.user.is_authenticated:
            cart_models = Cart.objects.filter(user_pk=self.request.user).annotate(image=Subquery(image_subquery),
                                                                                  total=Case(When(product__expensive_price=0, then=Value(F('product__price') * F('quantity')).value), default=Value(F('product__expensive_price') * F('quantity')).value))
            context['cart_models'] = cart_models
            context['cart_count'] = Cart.objects.filter(user_pk=self.request.user).count()
            cart_total = 0
            for i in cart_models:
                cart_total += i.total
            context['cart_total'] = cart_total
            if cart_total >= 100:
                context['services'] = 'Mugt'
                context['total'] = cart_total
            else:
                context['services'] = '10'
                context['total'] = cart_total + 10
        else:
            cart_models = Cart.objects.filter(anonymous_user=self.request.COOKIES.get('csrftoken')).annotate(image=Subquery(image_subquery),
                                                                                                             total=Case(When(product__expensive_price=0, then=Value(F('product__price') * F('quantity')).value), default=Value(F('product__expensive_price') * F('quantity')).value))
            context['cart_models'] = cart_models
            context['cart_count'] = Cart.objects.filter(anonymous_user=self.request.COOKIES.get('csrftoken')).count()
            cart_total = 0
            for i in cart_models:
                cart_total += i.total
            context['cart_total'] = cart_total
            if cart_total >= 100:
                context['services'] = 'Mugt'
                context['total'] = cart_total
            else:
                context['services'] = '10'
                context['total'] = cart_total + 10
        return context


class CheckoutView(TemplateView):
    template_name = 'app/checkout.html'

    def dispatch(self, request, *args, **kwargs):
        if self.get_context_data()['cart_count'] == 0:
            return HttpResponseRedirect(reverse('App:home'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        image_subquery = ProductImage.objects.filter(product_fk=OuterRef('product')).values('image')[:1]
        total_subquery = str(OuterRef('pk'))
        if self.request.user.is_authenticated:
            cart_models = Cart.objects.filter(user_pk=self.request.user).annotate(image=Subquery(image_subquery), total=Case(When(product__expensive_price=0, then=Value(F('product__price') * F('quantity')).value), default=Value(F('product__expensive_price') * F('quantity')).value))
            context['cart_models'] = cart_models
            context['cart_count'] = Cart.objects.filter(user_pk=self.request.user).count()
            cart_total = 0
            for i in cart_models:
                cart_total += i.total
            context['cart_total'] = cart_total
            if cart_total >= 100:
                context['services'] = 'Mugt'
                context['total'] = cart_total
            else:
                context['services'] = '10'
                context['total'] = cart_total + 10
        else:
            cart_models = Cart.objects.filter(anonymous_user=self.request.COOKIES.get('csrftoken')).annotate(image=Subquery(image_subquery),
                                                                                                             total=Case(When(product__expensive_price=0, then=Value(F('product__price') * F('quantity')).value), default=Value(F('product__expensive_price') * F('quantity')).value))
            context['cart_models'] = cart_models
            context['cart_count'] = Cart.objects.filter(anonymous_user=self.request.COOKIES.get('csrftoken')).count()
            cart_total = 0
            for i in cart_models:
                cart_total += i.total
            context['cart_total'] = cart_total
            if cart_total >= 100:
                context['services'] = 'Mugt'
                context['total'] = cart_total
            else:
                context['services'] = '10'
                context['total'] = cart_total + 10
        return context

    @staticmethod
    def post(request, *args, **kwargs):
        data = request.POST
        order = Order()
        if request.user.is_authenticated:
            order.user = request.user
        else:
            order.user = None
        order.phone_number = data['phone_number']
        order.address = data['address']
        order.payment_type = data.get('payment_method')
        if request.user.is_authenticated:
            cart_models = Cart.objects.filter(user_pk=request.user).annotate(total=Case(When(product__expensive_price=0, then=Value(F('product__price') * F('quantity')).value), default=Value(F('product__expensive_price') * F('quantity')).value))
            cart_total = 0
            for i in cart_models:
                cart_total += i.total
            order.total_price = cart_total
        else:
            cart_models = Cart.objects.filter(anonymous_user=request.COOKIES.get('csrftoken')).annotate(total=Case(When(product__expensive_price=0, then=Value(F('product__price') * F('quantity')).value), default=Value(F('product__expensive_price') * F('quantity')).value))
            cart_total = 0
            for i in cart_models:
                cart_total += i.total
            order.total_price = cart_total
        if cart_total >= 100:
            order.delivery_price = 0
        else:
            order.delivery_price = 10
        order.save()
        if request.user.is_authenticated:
            for i in Cart.objects.filter(user_pk=request.user):
                order_item = OrderItem()
                order_item.order = order
                order_item.product_fk = i.product
                order_item.cash_balance = i.product.cash_balance
                order_item.quantity = i.quantity
                order_item.name = i.product.name
                if i.product.expensive_price:
                    order_item.price = i.product.expensive_price
                else:
                    order_item.price = i.product.price
                order_item.save()
                i.delete()
        else:
            for i in Cart.objects.filter(anonymous_user=request.COOKIES.get('csrftoken')):
                order_item = OrderItem()
                order_item.order = order
                order_item.product_fk = i.product
                order_item.cash_balance = i.product.cash_balance
                order_item.quantity = i.quantity
                order_item.name = i.product.name
                order_item.price = i.product.price
                order_item.save()
                i.delete()
        return HttpResponseRedirect(reverse('App:home'))


class OrderHistoryView(ListView):
    template_name = 'app/order_history.html'
    model = Order
    paginate_by = 10
    context_object_name = 'models'

    def get_queryset(self):
        return Order.objects.all().order_by('-date')

    def get_paginate_by(self, queryset):
        limit_page = self.request.GET.get('limit', 10)
        return limit_page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = self.request.GET.get('page', '1')
        context['limit'] = self.request.GET.get('limit', 10)
        context['order_status_list'] = Order.order_status_list
        if self.request.user.is_authenticated:
            context['cart_count'] = Cart.objects.filter(user_pk=self.request.user).count()
        else:
            context['cart_count'] = Cart.objects.filter(anonymous_user=self.request.COOKIES.get('csrftoken')).count()
        return context

    @staticmethod
    def post(request, *args, **kwargs):
        print(request.POST.get('name'))
        order = Order.objects.get(name=request.POST.get('name'))
        order.order_state = '4'
        order.canceled_date = timezone.now()
        order.save()
        return JsonResponse({'message': 'success'}, status=200)


class OrderView(TemplateView):
    template_name = 'app/order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model = Order.objects.get(name=self.kwargs['code'])
        context['model'] = model
        image_subquery = ProductImage.objects.filter(product_fk=OuterRef('product_fk')).values('image')[:1]
        cart_models = OrderItem.objects.filter(order=model).annotate(image=Subquery(image_subquery), total=Value(F('price') * F('quantity')).value)
        context['cart_models'] = cart_models

        cart_total = 0
        for i in cart_models:
            cart_total += i.total
        context['cart_total'] = cart_total
        if cart_total >= 100:
            context['services'] = 'Mugt'
            context['total'] = cart_total
        else:
            context['services'] = '10'
            context['total'] = cart_total + 10
        if self.request.user.is_authenticated:
            context['cart_count'] = Cart.objects.filter(user_pk=self.request.user).count()
        else:
            context['cart_count'] = Cart.objects.filter(anonymous_user=self.request.COOKIES.get('csrftoken')).count()
        return context