from rest_framework import serializers
from users.models import User


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
        validated_data.pop('repeat_password')
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
