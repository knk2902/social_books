from rest_framework import serializers
from register.models import UploadedFiles
from .models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from djoser.serializers import UserCreateSerializer, UserSerializer


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            'first_name', 'last_name'
        )

    def create(self, validated_data):
        user = CustomUser.objects.create(username=validated_data['username'])
        user.det_password(validated_data['password'])

class CustomUserCreateSerializer(UserCreateSerializer):
    # email = serializers.CharField(
    #     required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    # )
    # password = serializers.CharField(
    #     write_only=True, required=True, validators=[validate_password]
    # )
    # password2 = serializers.CharField(write_only=True, required=True)

    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            "password",
            'fullname', 'dob', 'visibility',
        )
        
    # def validate(self, attrs):
    #     if attrs["password"] != attrs["password2"]:
    #         raise serializers.ValidationError(
    #             {"password": "Password fields didn't match."}
    #         )
    #     return attrs

    # def create(self, validated_data):
    #     user = CustomUser.objects.create(
    #         username=validated_data["username"],
    #         email=validated_data["email"],
    #         first_name=validated_data["first_name"],
    #         last_name=validated_data["last_name"],
    #     )
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFiles
        fields = [
            "id",
            "user",
            "file",
            "title",
            "description",
            "visibility",
            "cost",
            "year_published",
        ]
