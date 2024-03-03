from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    password = serializers.CharField(max_length=128, required=True)
