from django.urls import path
from users.password.views import ChangePasswordView, ValidateEmailAndResetPassword, ResetPasswordView

urlpatterns = [
    path('auth/change-password', ChangePasswordView.as_view()),
    path('auth/validate-email-and-reset-password',ValidateEmailAndResetPassword.as_view()),
    path('auth/reset_password', ResetPasswordView.as_view())

]