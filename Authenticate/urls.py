from django.urls import path

from Authenticate.views import *

app_name = 'Authenticate'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]