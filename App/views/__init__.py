from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView


class BaseTemplateView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser and request.user.user_type == '1':
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
        if request.user.is_authenticated and request.user.is_superuser and request.user.user_type == '1':
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('Authenticate:logout'))

    def get_paginate_by(self, queryset):
        limit_page = self.request.GET.get('limit', 10)
        return limit_page


class BaseCreateView(CreateView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser and request.user.user_type == '1':
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
        if request.user.is_authenticated and request.user.is_superuser and request.user.user_type == '1':
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('Authenticate:logout'))


class BaseView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser and request.user.user_type == '1':
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('Authenticate:logout'))

class Dashboard(BaseTemplateView):
    template_name = 'administrator/dashboard/index.html'
