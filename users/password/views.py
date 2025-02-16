from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from users.models import User
from users.password.serializers import ChangePasswordSerializer, ValidateEmailSerializer, ResetPasswordSerializer

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request):

        serializer = ChangePasswordSerializer(data=request.data, context={'request': request}, partial=True)

        if serializer.is_valid(raise_exception=True):
            user = request.user
            new_password = serializer.validated_data['new_password']

            user.set_password(new_password)
            user.save()

            return Response({'Message': 'Password changed successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValidateEmailAndResetPassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ValidateEmailSerializer(data=request.data, context={'request': request}, partial=True )
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()

            print(user)
            if user:
                #Genero un token unico
                reset_token = get_random_string(length=32)
                user.reset_password_token = reset_token
                user.save()

                #Enviar email para cabiar la contraseña
                reset_url = f"http://frontend-url.com/reset-password?token={reset_token}"
                send_mail(
                    subject="Password Reset Request",
                    message=f"Click the link to reset your password: {reset_url}",
                    from_email="no-reply@example.com",
                    recipient_list=[user.email],
                )

                return Response({"message": "Password reset link sent"}, status=status.HTTP_200_OK)
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']

            user = User.objects.get(reset_password_token = token)

            #Reestablecer la contraseña del
            user.set_password(new_password)
            user.reset_password_token = None
            user.save()

            return Response({'Message': 'Password reset successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
