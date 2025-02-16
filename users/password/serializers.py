from rest_framework import serializers
from users.models import User
from django.contrib.auth.hashers import check_password


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
        fields = ['id', 'email', 'username', 'password', 'new_password']

    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True, required=False)

    def validate_email(self,value):

        if not User.objects.filter(email=value):
            raise serializers.ValidationError('User with this email was not found')
        return value


class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'token', 'new_password']

    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

    def generate_token(self, value):
        if not User.objects.filter(reset_password_token=value).exists():
            raise serializers.ValidationError('Invalid Token or expired')
        return value
