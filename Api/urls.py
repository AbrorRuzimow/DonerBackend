from django.urls import include, path

from Api.views.authenticate import *
from Api.views.mobile import *

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/token/login/', CustomLoginView.as_view()),
    path('auth/token/logout/', CustomLogoutView.as_view()),
    path('auth/token/otp-code/', OTPView.as_view()),
    path('auth/token/otp-resend/', OTPReSend.as_view()),

    path('home-image/', HomePictureListAPI.as_view()),
    path('product/', ProductListAPI.as_view()),

    path('my-cart/', MyCartView.as_view()),
    path('add-cart/', AddCartView.as_view()),
    path('remove-cart/', RemoveCartView.as_view()),
    path('delete-cart/', DeleteCartView.as_view()),
    path('get-cart/', GetCartView.as_view()),
    path('wishlist/', WishListView.as_view()),
]
