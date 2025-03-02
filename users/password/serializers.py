from rest_framework import serializers
from users.models import User
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
import os
from dotenv import load_dotenv
import random

load_dotenv()
FRONTEND_URL = os.getenv("FRONTEND_URL")



class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'new_password']

    password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not check_password(value, user.password):
            raise serializers.ValidationError('Current Password is invalid')

        return value

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters')

        return value


class ValidateEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email']

    email = serializers.EmailField()
    # new_password = serializers.CharField(write_only=True, required=False)

    def validate_email(self,value):

        if not User.objects.filter(email=value):
            raise serializers.ValidationError('User with this email was not found')
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)

        #genero el nuevo token y el nuevo codigo
        reset_token = get_random_string(length=32)
        new_code = str(random.randint(100000, 999999))
        user.reset_password_token = reset_token
        user.verification_code = new_code
        user.save()

        #Enviar email para cambiar la contraseña
        reset_url = f"{FRONTEND_URL}/auth/new-password?email={user.email}&code={user.verification_code}"
        send_mail(
            subject="Password Reset Request",
            message=f"Click the link to reset your password: {reset_url} or write your code : {new_code}",
            from_email="no-reply@example.com",
            recipient_list=[user.email],
        )


class VerificateCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'verification_code']
    email = serializers.EmailField()
    verification_code = serializers.CharField(max_length=6)

    def validate(self,attrs):
        email = attrs.get('email')
        verification_code = attrs.get('verification_code')


        try:
            user = User.objects.get(email=email, verification_code=verification_code)

        except User.DoesNotExist:
            raise serializers.ValidationError({'message' : 'invalid mail or verification code'})

        return attrs



class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'verification_code', 'new_password', 'confirmation_password']

    email = serializers.EmailField()
    verification_code = serializers.CharField()
    new_password = serializers.CharField(min_length=8, write_only=True)
    confirmation_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        verification_code = attrs.get('verification_code')
        email = attrs.get('email')
        new_password = attrs.get('new_password')
        confirmation_password = attrs.get('confirmation_password')

        # Verificar que el código de verificación no sea None o vacío
        if not verification_code or verification_code == None:
            raise serializers.ValidationError({'verification_code': 'You must provide a verification code'})

        if new_password != confirmation_password:
            raise serializers.ValidationError({'message': 'Password do not match'})
        try:
            user = User.objects.get(email=email, verification_code=verification_code)
        except User.DoesNotExist:
            raise serializers.ValidationError({'message': 'User not found'})

        self.user = user  # Guardamos la instancia del usuario validado
        return attrs

    def update(self, instance, validated_data):
        # Usamos `update` para modificar el usuario existente
        instance.set_password(validated_data['new_password'])  # Actualiza la contraseña
        instance.verification_code = None  # Opcional: Limpiar el código de verificación
        instance.reset_password_token = get_random_string(length=32)  # Nuevo token
        instance.save()  # Guardamos la instancia con los cambios
        return instance



