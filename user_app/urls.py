from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('auth/register/', views.register_view, name='auth_register'),
    path('auth/login/', views.login_view, name='auth_login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', views.logout_view, name='auth_logout'),
    path('auth/change-password/', views.change_password_view, name='auth_change_password'),
    path('auth/me/', views.current_user_view, name='auth_current_user'),
]
