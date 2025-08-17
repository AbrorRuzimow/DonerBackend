from django.contrib import messages
from django.db.models import Value, F, OuterRef, Subquery
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView

from App.models import Order, OrderItem, ProductImage


class BaseTemplateView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == '2':
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('Authenticate:logout'))


class BaseListView(ListView):
    context_object_name = 'models'
    paginate_by = 10
    model = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = self.request.GET.get('page', '1')
        context['search'] = self.request.GET.get('search', '')
        context['order_by'] = self.request.GET.get('order_by', '')
        context['limit'] = self.request.GET.get('limit', 10)
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == '2':
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('Authenticate:logout'))

    def get_paginate_by(self, queryset):
        limit_page = self.request.GET.get('limit', 10)
        return limit_page


class BaseCreateView(CreateView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == '2':
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('Authenticate:logout'))

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Maglumat girizildi")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, f"Ýalňyşlyk ýüze çykdy: {form.errors}")
        return response


class BaseUpdateView(UpdateView):
    context_object_name = 'model'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Maglumat üýtgedildi")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.success(self.request, "Ýalňyşlyk ýüze çykdy")
        return response

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == '2':
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('Authenticate:logout'))


class BaseView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == '2':
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('Authenticate:logout'))


class Dashboard(BaseTemplateView):
    template_name = 'manager/index.html'


class OrderListView(BaseListView):
    template_name = 'manager/order/list.html'
    context_object_name = 'models'

    def get_queryset(self):
        models = Order.objects.all()
        if self.request.GET.get('search'):
            models = models.filter(name__icontains=self.request.GET.get('search'))
        if self.request.GET.get('status'):
            models = models.filter(order_state__in=self.request.GET.get('status').split(','))
        return models

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_status_list'] = Order.order_status_list
        context['models_all'] = self.get_queryset().count()
        context['order_status_list'] = Order.order_status_list
        context['payment_type_list'] = Order.payment_type_list
        context['order_status'] = self.request.GET.get('status', '').split(',')
        return context


class OrderDetailView(BaseTemplateView):
    template_name = 'manager/order/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        models = Order.objects.get(name=self.kwargs['code'])
        context['models'] = models
        context['order_status_list'] = Order.order_status_list
        context['payment_type_list'] = Order.payment_type_list
        image_subquery = ProductImage.objects.filter(product_fk=OuterRef('product_fk')).values('image')[:1]
        context['order_models'] = OrderItem.objects.filter(order=models).annotate(image=Subquery(image_subquery), total=Value(F('price') * F('quantity')).value)
        return context


class OrderRegister(BaseView):
    @staticmethod
    def get(request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['pk'])
        order.order_state = 2
        order.save()
        return HttpResponseRedirect(reverse('Manager:order_detail_list', args={order.name}))


class OrderCancel(BaseView):
    @staticmethod
    def get(request, *args, **kwargs):
        print(kwargs['pk'])
        order = Order.objects.get(id=kwargs['pk'])
        order.order_state = 5
        order.save()
        return HttpResponseRedirect(reverse('Manager:order_detail_list', args={order.name}))

class OrderSuccess(BaseView):
    @staticmethod
    def get(request, *args, **kwargs):
        print(kwargs['pk'])
        order = Order.objects.get(id=kwargs['pk'])
        order.order_state = 3
        order.save()
        return HttpResponseRedirect(reverse('Manager:order_detail_list', args={order.name}))


def product_cash_back(product):
    return