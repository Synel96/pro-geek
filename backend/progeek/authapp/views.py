from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
import datetime
from .serializers import RegistrationSerializer
from core.models import RegistrationCode
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny

class CookieTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            data = response.data
            access = data.get('access')
            refresh = data.get('refresh')
            expires = timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            refresh_expires = timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
            response.set_cookie('access', access, httponly=True, samesite='Lax', expires=expires)
            response.set_cookie('refresh', refresh, httponly=True, samesite='Lax', expires=refresh_expires)
            response.data = {'detail': 'Login successful'}
        return response

class CookieTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get('refresh')
        if not refresh:
            return Response({'detail': 'No refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
        request.data['refresh'] = refresh
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access = response.data.get('access')
            expires = timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            response.set_cookie('access', access, httponly=True, samesite='Lax', expires=expires)
            response.data = {'detail': 'Token refreshed'}
        return response

class CookieLogoutView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        response = Response({'detail': 'Logged out'}, status=204)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response

class RegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                code_val = request.data.get('registration_code')
                email = request.data.get('email')
                send_mail(
                    'Fiók aktiválása',
                    f'Köszönjük a regisztrációt! Az aktiváláshoz használd ezt a kódot: {code_val}',
                    None,
                    [email],
                    fail_silently=True
                )
                if code_val:
                    try:
                        code_obj = RegistrationCode.objects.get(code=code_val, is_used=False)
                        code_obj.is_used = True
                        code_obj.used_at = timezone.now()
                        code_obj.save()
                    except RegistrationCode.DoesNotExist:
                        pass
            except ValueError as e:
                return Response({'registration_code': [str(e)]}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationCodeCheckView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        code = request.data.get('registration_code')
        if not code:
            return Response({'detail': 'No code provided.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            code_obj = RegistrationCode.objects.get(code=code, is_used=False)
            return Response({'valid': True}, status=status.HTTP_200_OK)
        except RegistrationCode.DoesNotExist:
            return Response({'valid': False, 'detail': 'Invalid or already used code.'}, status=status.HTTP_400_BAD_REQUEST)

class ActivateUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        code = request.data.get('activation_code')
        User = get_user_model()
        try:
            user = User.objects.get(username=username, is_active=False)
            if user.registration_code and user.registration_code.code == code:
                user.is_active = True
                user.save()
                return Response({'detail': 'Fiók aktiválva.'}, status=200)
            else:
                return Response({'detail': 'Hibás aktivációs kód.'}, status=400)
        except User.DoesNotExist:
            return Response({'detail': 'Felhasználó nem található vagy már aktív.'}, status=404)

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            send_mail(
                'Jelszó visszaállítás',
                f'Jelszó visszaállításához használd ezt a kódot: {token}',
                None,
                [email],
                fail_silently=True
            )
            return Response({'reset_token': token, 'username': user.username}, status=200)
        except User.DoesNotExist:
            return Response({'detail': 'Nincs ilyen email.'}, status=404)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        token = request.data.get('reset_token')
        new_password = request.data.get('new_password')
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({'detail': 'Jelszó sikeresen módosítva.'}, status=200)
            else:
                return Response({'detail': 'Érvénytelen token.'}, status=400)
        except User.DoesNotExist:
            return Response({'detail': 'Felhasználó nem található.'}, status=404)
