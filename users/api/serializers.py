from rest_framework import serializers
from users.models import User
import random
from django.core.mail import send_mail



class UserRegisterSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'repeat_password']
        extra_kwargs =  {'password': {'write_only': True}}

    def validate(self, data):
        errors = {}

        if data.get('password') != data.get('repeat_password'):
            errors['repeat_password'] = ['Passwords do not match']

        if User.objects.filter(email=data.get('email')).exists():
            errors['email'] = ['This email is already in use']

        if User.objects.filter(username=data.get('username')).exists():
            errors['username'] = ['This username is already in use']

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        print(f'Que tiene el validated_data {validated_data}')
        validated_data.pop('repeat_password')
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        print(f' Viendo como se forma la instancia del usuario {instance}')
        if password is not None:
            instance.set_password(password)

        instance.generate_verification_code()

        send_mail(
            subject="Confirm your account",
            message=f"Your code to verify your account: {instance.verification_code}",
            from_email="serggio.c86@gmail.com",
            recipient_list=[instance.email],
        )


        instance.save()
        return instance

class VerifyCodeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    verification_code = serializers.CharField(max_length=6)
    class Meta:
        model = User
        fields = ['id', 'email', 'verification_code']

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'], verification_code=data['verification_code'])
        except User.DoesNotExist:
            raise serializers.ValidationError({'error': 'Wrong Code'})

        return data

    def save(self):
        user = User.objects.get(email=self.validated_data["email"])
        user.is_verified = True
        user.verification_code = None
        user.save()


class ReSendCodeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['id', 'email']

    def validate(self, data):
        print(f'🟢 Llega la data al serializer? {data}')
        try:
            user = User.objects.get(email=data['email'])
            print(f'🔵 Usuario encontrado: {user}')
            if user.is_verified:
                raise serializers.ValidationError({'error': 'User already verified'})
        except User.DoesNotExist:
            print(f' No se encontró el usuario con email: {data["email"]}')
            raise serializers.ValidationError({'error': 'User Not found'})

        return data

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])

        #genero el nuevo codigo
        new_code = str(random.randint(100000, 999999))
        user.verification_code = new_code
        user.save()

        send_mail(
            subject="Confirm your code",
            message=f"Your code to verify your account: {new_code}",
            from_email="serggio.c86@gmail.com",
            recipient_list=[user.email],
        )






class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
