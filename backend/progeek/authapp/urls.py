from django.urls import path
from .views import CookieTokenObtainPairView, CookieTokenRefreshView, CookieLogoutView, RegistrationView, RegistrationCodeCheckView

urlpatterns = [
    path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', CookieLogoutView.as_view(), name='token_logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('check-code/', RegistrationCodeCheckView.as_view(), name='check_code'),
]
