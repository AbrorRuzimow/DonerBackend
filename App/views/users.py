from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy

from App.models import Users
from App.views import *


class UsersList(BaseListView):
    template_name = 'administrator/users/list.html'

    def get_queryset(self):
        models = Users.objects.all()
        if self.request.GET.get('user_type') and self.request.GET.get('user_type') != '0':
            models = models.filter(user_type=self.request.GET.get('user_type'))
        if self.request.GET.get('search'):
            models = models.filter(phone_number__icontains=self.request.GET.get('search'))
        return models

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type_value'] = self.request.GET.get('user_type', 0)
        context['user_type_list'] = Users.user_type_list
        context['models_all'] = self.get_queryset().count()
        return context


class UsersCreate(BaseCreateView):
    template_name = 'administrator/users/create.html'
    model = Users
    fields = ('phone_number',)

    def post(self, request, *args, **kwargs):
        user = Users()
        try:
            user.username = request.POST.get('username')
            user.phone_number = request.POST.get('phone_number')
            user.set_password(request.POST.get('password'))
            user.user_type = request.POST.get('user_type')
            user.save()
        except Exception as e:
            print(e)
        return HttpResponseRedirect(reverse('Administrator:users_list'))


class UsersUpdate(BaseUpdateView):
    template_name = 'administrator/users/update.html'
    model = Users
    fields = ('phone_number',)
    success_url = reverse_lazy('Administrator:users_list')

    def post(self, request, *args, **kwargs):
        try:
            user = Users.objects.get(id=self.kwargs.get('pk'))
            user.username = request.POST.get('username')
            user.phone_number = request.POST.get('phone_number')
            user.user_type = request.POST.get('user_type')
            user.save()
        except Exception as e:
            print(e)
        return HttpResponseRedirect(reverse('Administrator:users_list'))


class UsersDelete(BaseView):
    @staticmethod
    def get(request, *args, **kwargs):
        try:
            Users.objects.get(pk=kwargs['pk']).delete()
            messages.success(request, "Maglumat pozuldy")
        except ObjectDoesNotExist:
            messages.error(request, "Ýalňyşlyk ýüze çykdy")
        return HttpResponseRedirect(reverse('Administrator:users_list'))


class UsersMultiDelete(BaseView):
    @staticmethod
    def post(request, *args, **kwargs):
        for i in request.POST.getlist('item_id'):
            try:
                Users.objects.get(pk=i).delete()
                messages.success(request, "Maglumat pozuldy")
            except ObjectDoesNotExist:
                messages.error(request, "Ýalňyşlyk ýüze çykdy")
        return HttpResponseRedirect(reverse('Administrator:users_list'))
