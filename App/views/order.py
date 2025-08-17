from django.db.models import OuterRef, Subquery, Value, F

from App.models import *
from App.views import *


class OrderListView(BaseListView):
    template_name = 'administrator/order/list.html'
    context_object_name = 'models'

    def get_queryset(self):
        models = Order.objects.all().order_by('-date').order_by('order_state')
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
    template_name = 'administrator/order/detail.html'

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
        return HttpResponseRedirect(reverse('Administrator:order_detail_list', args={order.name}))


class OrderCancel(BaseView):
    @staticmethod
    def get(request, *args, **kwargs):
        print(kwargs['pk'])
        order = Order.objects.get(id=kwargs['pk'])
        order.order_state = 5
        order.save()
        return HttpResponseRedirect(reverse('Administrator:order_detail_list', args={order.name}))


def calc_cash_balance(product):
    money = 0.0
    money = (product.price - product.cost) * product.cash_balance / 100
    return money


class OrderSuccess(BaseView):
    @staticmethod
    def get(request, *args, **kwargs):

        order = Order.objects.get(id=kwargs['pk'])
        order.order_state = 3
        order.save()
        if order.user:
            for i in OrderItem.objects.filter(order=order):
                for c in range(0, i.quantity):
                    money = calc_cash_balance(i.product_fk)
                    payment = Payment()
                    payment.user_fk = order.user
                    payment.order = i
                    payment.money = money
                    payment.save()
                    users = Users.objects.get(pk=order.user_id)
                    users.wallet += money
                    users.save()
                    for w in ProductWarehouse.objects.filter(product_fk=i.product_fk):
                        print(f'{w.product_fk.name} + {w.warehouse_name_fk.name} == {w.amount}')
                        active_warehouse = Warehouse.objects.filter(warehouse_name_fk=w.warehouse_name_fk, status='1').order_by('-date')[:1].first()
                        print(f'{active_warehouse.warehouse_name_fk.name} + {active_warehouse.amount_use}')
                        if active_warehouse.amount_use + w.amount > active_warehouse.amount:
                            print('-----------------------------------')
                            amount_use = active_warehouse.amount - active_warehouse.amount_use
                            active_warehouse.active_warehouse.amount_use += amount_use
                            amount = active_warehouse.amount_use + w.amount - active_warehouse.amount
                            active_warehouse.status = '2'
                            active_warehouse.save()
                            active_warehouse = Warehouse.objects.filter(warehouse_name_fk=w.warehouse_name_fk, status='1').order_by('-date')[:1].first()
                            if active_warehouse:
                                active_warehouse.amount_use += amount
                                active_warehouse.save()
                            else:
                                # Name etmeli eger ammarda produkta gutarsa? TEKLIP!
                                pass
                        elif active_warehouse.amount_use + w.amount == active_warehouse.amount:
                            print('-----------------------------------')
                            active_warehouse.amount_use += w.amount
                            active_warehouse.status = '2'
                            active_warehouse.save()
                        else:
                            print('-----------------------------------')
                            active_warehouse.amount_use += w.amount
                            active_warehouse.save()
        return HttpResponseRedirect(reverse('Administrator:order_detail_list', args={order.name}))
