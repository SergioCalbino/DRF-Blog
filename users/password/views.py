from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import check_password
from users.models import User
from users.password.serializers import ChangePasswordSerializer, ValidateEmailSerializer, ResetPasswordSerializer, VerificateCodeSerializer

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
    # permission_classes = [AllowAny]

    def post(self, request):

        serializer = ValidateEmailSerializer(data=request.data, context={'request': request}, partial=True )
        if serializer.is_valid():
            serializer.save()

            return Response({'message': 'Email was send with instrucctions'}, status=status.HTTP_200_OK)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class VerificationCodeView(APIView):
    def post(self, request):
        serializer = VerificateCodeSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': 'Your code is correct, set new password'}, status=status.HTTP_200_OK)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)





class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)  # No buscar al usuario aquí

        if serializer.is_valid():
            user = serializer.user  # El usuario ya está validado en el serializer
            serializer.update(user, serializer.validated_data)
            return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
