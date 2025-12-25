from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from Api.models import Product, HomePicture, Cart, WishList
from Api.serializers import ProductSerializer, HomePictureSerializer, CartSerializer, WishListSerializers


class HomePictureListAPI(APIView):
    @staticmethod
    def get(request):
        models = HomePicture.objects.all()
        serializer = HomePictureSerializer(models, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductListAPI(APIView):
    @staticmethod
    def get(request):
        products = Product.objects.filter(is_active=True).prefetch_related('images')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyCartView(APIView):
    @staticmethod
    def get(request):
        models = Cart.objects.filter(user_pk=request.user.pk)
        return Response({'cartCount': models.count()}, status=status.HTTP_200_OK)


class AddCartView(APIView):
    @staticmethod
    def post(request):
        data = request.data
        try:
            product = Product.objects.get(id=data['product'])
        except:
            return Response({'message': 'Haryt tapylmady'}, status=status.HTTP_404_NOT_FOUND)
        try:
            cart_item = Cart.objects.get(user_pk=request.user, product=product)
            cart_item.quantity += data['quantity']
            cart_item.save()
            return Response({'message': 'Haryt goşuldy'}, status=status.HTTP_200_OK)
        except:
            Cart.objects.create(user_pk=request.user, product=product, quantity=data['quantity'])
            return Response({'message': 'Haryt goşuldy'}, status=status.HTTP_201_CREATED)


class RemoveCartView(APIView):
    @staticmethod
    def post(request):
        data = request.data
        try:
            product = Product.objects.get(id=data['product'])
        except:
            return Response({'message': 'Haryt tapylmady'}, status=status.HTTP_404_NOT_FOUND)
        cart_item = Cart.objects.get(user_pk=request.user, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= data['quantity']
            cart_item.save()
        else:
            cart_item.delete()
        return Response({'message': 'Haryt aýryldy'}, status=status.HTTP_200_OK)

class DeleteCartView(APIView):
    @staticmethod
    def post(request):
        data = request.data
        try:
            product = Product.objects.get(id=data['product'])
        except:
            return Response({'message': 'Haryt tapylmady'}, status=status.HTTP_404_NOT_FOUND)
        cart_item = Cart.objects.get(user_pk=request.user, product=product)
        cart_item.delete()
        return Response({'message': 'Haryt aýryldy'}, status=status.HTTP_200_OK)


class GetCartView(APIView):
    def get(self, request):
        carts = (
            Cart.objects
            .filter(user_pk=request.user)
            .select_related('product')
            .prefetch_related('product__images')
        )
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class WishListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        product_id = request.query_params.get('id')
        if not user_id or not product_id:
            return Response({'message': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        wishlist_item, created = WishList.objects.get_or_create(user_fk_id=user_id, product_fk=product)

        if created:
            return Response({'message': 'Product added to wish list'}, status=status.HTTP_201_CREATED)
        else:
            wishlist_item.delete()
            return Response({'message': 'Product remove from wish list'}, status=status.HTTP_204_NO_CONTENT)

class GetWishList(generics.ListAPIView):
    serializer_class = WishListSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WishList.objects.filter(userId=self.request.user)