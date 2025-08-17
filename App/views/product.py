from django.core.exceptions import ObjectDoesNotExist
from django.db.models import OuterRef, Subquery, Case, When, Value, IntegerField, F, ExpressionWrapper, DecimalField
from django.http import JsonResponse
from django.urls import reverse_lazy

from App.models import Product, ProductImage, ProductWarehouse, Warehouse, WarehouseName
from App.views import *


class ProductList(BaseListView):
    template_name = 'administrator/product/list.html'

    def get_queryset(self):
        image_subquery = ProductImage.objects.filter(product_fk=OuterRef('pk')).values('image')[:1]
        return Product.objects.all().order_by('-id').annotate(image=Subquery(image_subquery),
                                                              display_percentage=Case(When(percentage=0, then=Value(False)), default=F('percentage'), output_field=IntegerField()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_list'] = Product.status_list
        context['models_all'] = Product.objects.all().count()
        return context


class ProductCreate(BaseCreateView):
    template_name = 'administrator/product/create.html'
    model = Product
    fields = ('name',)
    success_url = reverse_lazy('Administrator:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_list'] = Product.status_list
        return context

    def post(self, request, *args, **kwargs):
        try:
            data = self.request.POST
            model = Product()
            model.name = data['name']
            model.cash_balance = data['cash_balance']
            model.description = data['description']
            model.price = data['price']
            model.status = data['status']
            model.description = data['description']
            if data['discount_option'] == '1':
                pass
            elif data['discount_option'] == '2':
                model.percentage = data['percentage']
            elif data['discount_option'] == '3':
                model.expensive_price = data['expensive_price']
            else:
                pass
            model.save()
            if self.request.FILES:
                for i in self.request.FILES.getlist('images'):
                    image_model = ProductImage()
                    image_model.product_fk = model
                    image_model.image = i
                    image_model.save()
            return JsonResponse({'message': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)


class ProductUpdate(BaseUpdateView):
    template_name = 'administrator/product/update.html'
    model = Product
    fields = ('name',)
    success_url = reverse_lazy('Administrator:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_list'] = Product.status_list
        return context

    def post(self, request, *args, **kwargs):
        try:
            data = self.request.POST
            model = Product.objects.get(pk=self.kwargs['pk'])
            model.name = data['name']
            model.cash_balance = data['cash_balance']
            model.description = data['description']
            model.price = data['price']
            model.status = data['status']
            model.description = data['description']
            if data['discount_option'] == '1':
                pass
            elif data['discount_option'] == '2':
                model.percentage = data['percentage']
                model.expensive_price = 0
            elif data['discount_option'] == '3':
                model.percentage = 0
                model.expensive_price = data['expensive_price']
            else:
                pass
            model.save()
            if self.request.FILES:
                for i in self.request.FILES.getlist('images'):
                    image_model = ProductImage()
                    image_model.product_fk = model
                    image_model.image = i
                    image_model.save()
            return JsonResponse({'message': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)


class ProductDelete(BaseView):
    @staticmethod
    def get(request, *args, **kwargs):
        try:
            Product.objects.get(pk=kwargs['pk']).delete()
            messages.success(request, "Maglumat pozuldy")
        except ObjectDoesNotExist:
            messages.error(request, "Ýalňyşlyk ýüze çykdy")
        return HttpResponseRedirect(reverse('Administrator:product_list'))


class ProductMultiDelete(BaseView):
    @staticmethod
    def post(request, *args, **kwargs):
        for i in request.POST.getlist('item_id'):
            try:
                Product.objects.get(pk=i).delete()
                messages.success(request, "Maglumat pozuldy")
            except ObjectDoesNotExist:
                messages.error(request, "Ýalňyşlyk ýüze çykdy")
        return HttpResponseRedirect(reverse('Administrator:product_list'))


class ProductWarehouseList(BaseListView):
    template_name = 'administrator/product/warehouse/list.html'
    context_object_name = 'models'

    def get_queryset(self):
        active_warehouse = Warehouse.objects.filter(warehouse_name_fk=OuterRef('warehouse_name_fk'), status='1').order_by('-date')
        one_price = ExpressionWrapper(F('price') / F('amount'), output_field=DecimalField(max_digits=10, decimal_places=2))
        subquery = active_warehouse.annotate(amount_div_price=one_price).values('amount_div_price')[:1]
        return ProductWarehouse.objects.filter(product_fk__id=self.kwargs['pk']).annotate(price=Subquery(subquery), total=Value(Subquery(subquery) * F('amount')).value)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(pk=self.kwargs['pk'])
        context['product'] = product
        context['pk'] = self.kwargs['pk']
        context['count'] = self.get_queryset().count()
        context['my_cash_balance'] = (product.price - product.cost) * product.cash_balance / 100
        return context


class ProductCashBackView(BaseTemplateView):
    template_name = 'administrator/product/warehouse/cash_back.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['models'] = Product.objects.get(pk=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        model = Product.objects.get(pk=self.kwargs['pk'])
        model.cash_balance = request.POST['cash_balance']
        model.save()
        return JsonResponse({'message': 'success'}, status=200)


class ProductWarehouseCreate(BaseTemplateView):
    template_name = 'administrator/product/warehouse/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['warehouse_models'] = WarehouseName.objects.all()
        context['pk'] = self.kwargs['pk']
        return context

    @staticmethod
    def post(request, *args, **kwargs):
        data = request.POST
        model = ProductWarehouse()
        model.product_fk_id = kwargs['pk']
        model.warehouse_name_fk_id = data['warehouse']
        model.amount = data['amount']
        model.save()
        total = 0
        active_warehouse = Warehouse.objects.filter(warehouse_name_fk=OuterRef('warehouse_name_fk'), status='1').order_by('-date')
        one_price = ExpressionWrapper(F('price') / F('amount'), output_field=DecimalField(max_digits=10, decimal_places=2))
        subquery = active_warehouse.annotate(amount_div_price=one_price).values('amount_div_price')[:1]
        for i in ProductWarehouse.objects.filter(product_fk__id=kwargs['pk']).annotate(price=Subquery(subquery), total=Value(Subquery(subquery) * F('amount')).value):
            try:
                total += i.total
            except:
                total += 0
        product = Product.objects.get(pk=kwargs['pk'])
        product.cost = total
        product.price_cost = product.price - total
        product.save()
        return HttpResponseRedirect(reverse('Administrator:product_warehouse_list', args=[model.product_fk.id]))


class ProductWarehouseUpdate(BaseTemplateView):
    template_name = 'administrator/product/warehouse/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['models'] = ProductWarehouse.objects.get(pk=self.kwargs['pk'])
        context['warehouse_models'] = WarehouseName.objects.all()
        return context

    @staticmethod
    def post(request, *args, **kwargs):
        data = request.POST
        model = ProductWarehouse.objects.get(pk=kwargs['pk'])
        model.warehouse_name_fk_id = data['warehouse']
        model.amount = data['amount']
        model.save()
        total = 0
        active_warehouse = Warehouse.objects.filter(warehouse_name_fk=OuterRef('warehouse_name_fk'), status='1').order_by('-date')
        one_price = ExpressionWrapper(F('price') / F('amount'), output_field=DecimalField(max_digits=10, decimal_places=2))
        subquery = active_warehouse.annotate(amount_div_price=one_price).values('amount_div_price')[:1]
        for i in ProductWarehouse.objects.filter(product_fk=model.product_fk).annotate(price=Subquery(subquery), total=Value(Subquery(subquery) * F('amount')).value):
            try:
                total += i.total
            except:
                total += 0
        product = Product.objects.get(pk=model.product_fk_id)
        product.cost = total
        product.price_cost = product.price - total
        product.save()
        return HttpResponseRedirect(reverse('Administrator:product_warehouse_list', args=[model.product_fk.id]))


class ProductWarehouseDelete(BaseView):
    @staticmethod
    def get(request, *args, **kwargs):
        try:
            model = (ProductWarehouse.objects.get(pk=kwargs['pk']))
            pk = model.product_fk_id
            model.delete()
            total = 0
            active_warehouse = Warehouse.objects.filter(warehouse_name_fk=OuterRef('warehouse_name_fk'), status='1').order_by('-date')
            one_price = ExpressionWrapper(F('price') / F('amount'), output_field=DecimalField(max_digits=10, decimal_places=2))
            subquery = active_warehouse.annotate(amount_div_price=one_price).values('amount_div_price')[:1]
            for i in ProductWarehouse.objects.filter(product_fk_id=pk).annotate(price=Subquery(subquery), total=Value(Subquery(subquery) * F('amount')).value):
                try:
                    total += i.total
                except:
                    total += 0
            product = Product.objects.get(pk=pk)
            product.cost = total
            product.price_cost = product.price - total
            product.save()
            messages.success(request, "Maglumat pozuldy")
            return HttpResponseRedirect(reverse('Administrator:product_warehouse_list', args=[pk]))
        except ObjectDoesNotExist:
            messages.error(request, "Ýalňyşlyk ýüze çykdy")
            return HttpResponseRedirect(reverse('Administrator:product_list'))
