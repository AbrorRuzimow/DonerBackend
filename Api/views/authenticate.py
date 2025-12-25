import datetime
import random

from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()


def result_phone(phoneNumber: str) -> bool:
    if len(phoneNumber) != 8:
        return False
    if phoneNumber[0] == '6':
        if phoneNumber[1] not in ('1', '2', '3', '4''5'):
            return False
    elif phoneNumber[0] == '7':
        if phoneNumber[1] not in ('1'):
            return False
    if phoneNumber[0] not in ('6', '7'):
        return False
    return True


# Custom Login View -> error message
class CustomLoginView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
            user_generate_otp(user)
            return Response({'message': 'Dogry'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            if result_phone(username):
                user = User.objects.create(username=username)
                user_generate_otp(user)
                return Response({'message': 'Hasaba alyndy!'}, status=status.HTTP_200_OK)
            return Response({'message': 'Telefon belgi ýalňyş!'}, status=status.HTTP_400_BAD_REQUEST)


# Custom logout
class CustomLogoutView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


# Generate OTP Code -> 30 seconds
def user_generate_otp(user):
    user.otp_code = str(random.randint(100000, 999999))
    user.otp_is_active = True
    user.otp_expires = timezone.now() + datetime.timedelta(seconds=30)
    user.save()
    return


class OTPView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        username = request.data.get('username')
        code = request.data.get('code')
        if not username:
            return Response({'message': 'Phone number invalid'}, status=status.HTTP_400_BAD_REQUEST)
        if not code:
            return Response({'message': 'Code invalid'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
            if user.otp_code != code:
                return Response({'message': 'Kod ýalňyş'}, status=status.HTTP_400_BAD_REQUEST)
            elif str(user.otp_code) == str(code) and timezone.now() <= user.otp_expires:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'message': token.key}, status=status.HTTP_200_OK)
            elif str(user.otp_code) == str(code) and timezone.now() >= user.otp_expires:
                return Response({'message': 'Berlen wagt tamamlandy'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Kod ýalňyş'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'Telefon belgi nädogry'}, status=status.HTTP_400_BAD_REQUEST)


class OTPReSend(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
            user_generate_otp(user)
            return Response({'message': 'Kod ugradyldy'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'Telefon belgi nädogry'}, status=status.HTTP_400_BAD_REQUEST)
