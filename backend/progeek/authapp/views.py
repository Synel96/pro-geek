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

class CookieTokenObtainPairView(TokenObtainPairView):
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
    def post(self, request):
        response = Response({'detail': 'Logged out'}, status=200)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response

class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except ValueError as e:
                return Response({'registration_code': [str(e)]}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationCodeCheckView(APIView):
    def post(self, request):
        code = request.data.get('registration_code')
        if not code:
            return Response({'detail': 'No code provided.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            code_obj = RegistrationCode.objects.get(code=code, is_used=False)
            return Response({'valid': True}, status=status.HTTP_200_OK)
        except RegistrationCode.DoesNotExist:
            return Response({'valid': False, 'detail': 'Invalid or already used code.'}, status=status.HTTP_400_BAD_REQUEST)
