from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'username']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, help_text="Username or Email address")
    password = serializers.CharField(required=True, write_only=True)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True, help_text="JWT Refresh Token to blacklist")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({"password": "Password and Confirm Password do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=6)
    confirm_new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('confirm_new_password'):
            raise serializers.ValidationError({"new_password": "New Password and Confirm New Password do not match."})
        return attrs
