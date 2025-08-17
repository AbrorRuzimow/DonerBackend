from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from App.models import Users


class BaseTemplateView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.POST.get('next', None):
                return HttpResponseRedirect(request.POST['next'])
            if request.user.user_type == '1':
                return HttpResponseRedirect(reverse('Administrator:dashboard'))
            elif request.user.user_type == '2':
                return HttpResponseRedirect(reverse('Manager:dashboard'))
            elif request.user.user_type == '3':
                return HttpResponseRedirect(reverse('App:home'))
            return HttpResponseRedirect(reverse('Authenticate:logout'))
        else:
            return super().dispatch(request, *args, **kwargs)


class LoginView(BaseTemplateView):
    template_name = 'authenticate/login.html'

    @staticmethod
    def post(request, *args, **kwargs):
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            print(request.user.user_type)
            if request.POST.get('next', None):
                return HttpResponseRedirect(request.POST['next'])
            if request.user.user_type == '1':
                return HttpResponseRedirect(reverse('Administrator:dashboard'))
            elif request.user.user_type == '2':
                return HttpResponseRedirect(reverse('Manager:dashboard'))
            elif request.user.user_type == '3':
                return HttpResponseRedirect(reverse('App:home'))
            return HttpResponseRedirect(reverse('Authenticate:logout'))

        else:
            return HttpResponseRedirect(reverse('Authenticate:login'))


class AppLoginView(BaseTemplateView):
    template_name = 'app/login.html'

    @staticmethod
    def post(request, *args, **kwargs):
        user = authenticate(request, username=request.POST['phone_number'], password=request.POST['password'])
        if user is not None and user.phone_number == request.POST['phone_number']:
            login(request, user)
            if request.POST.get('next', None):
                return HttpResponseRedirect(request.POST['next'])
            if request.user.user_type == '1':
                return HttpResponseRedirect(reverse('Administrator:dashboard'))
            elif request.user.user_type == '2':
                return HttpResponseRedirect(reverse('Manager:dashboard'))
            elif request.user.user_type == '3':
                return HttpResponseRedirect(reverse('App:home'))
            return HttpResponseRedirect(reverse('Authenticate:logout'))
        else:
            return HttpResponseRedirect(reverse('App:login'))


class AppRegisterView(BaseTemplateView):
    template_name = 'app/register.html'

    @staticmethod
    def post(request, *args, **kwargs):
        data = request.POST
        try:
            Users.objects.get(username=data['phone_number'])
            messages.error(request, 'Siz öň agza bolduňyz')
            return HttpResponseRedirect(reverse('App:register'))
        except:
            pass
        try:
            user = Users()
            user.phone_number = data['phone_number']
            user.username = data['phone_number']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.set_password(data['password'])
            user.user_type = 3
            user.save()
            messages.success(request, 'Agza bolduňyz')
            return HttpResponseRedirect(reverse('App:login'))
        except:
            messages.error(request, 'Ýalňyşlyk ýüze çykdy')
            return HttpResponseRedirect(reverse('App:register'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('App:home'))
