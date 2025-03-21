from django.urls import path
from users.api.views import RegisterView, UserView, UserShowAll, VerifyCodeView, ReSendCodeView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('auth/register', RegisterView.as_view()),
    path('auth/verify', VerifyCodeView.as_view()),
    path('auth/re-send-code', ReSendCodeView.as_view()),
    path('auth/login', TokenObtainPairView.as_view()),
    path('auth/token/refresh', TokenRefreshView.as_view()),
    path('auth/me', UserView.as_view()),
    path('auth/show', UserShowAll.as_view()),
]
