from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from Api.models import *

User = get_user_model()


# auth/users/me/ Custom User Serializers -> id, username, wallet
class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'username', 'wallet')


class HomePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePicture
        fields = ['image']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)  # barcha rasmlar

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'expensive_price', 'percentage', 'cash_balance', 'images']


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'product', 'quantity']


class WishListSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    name = serializers.ReadOnlyField(source='product.name')
    description = serializers.ReadOnlyField(source='product.description')
    price = serializers.ReadOnlyField(source='product.price')

    class Meta:
        model = WishList
        fields = ['id', 'name', 'description', 'price']
