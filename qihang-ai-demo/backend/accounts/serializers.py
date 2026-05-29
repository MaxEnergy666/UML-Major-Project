from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """用户信息序列化器"""

    class Meta:
        model = User
        fields = ["id", "username", "phone", "name", "role", "is_verified"]
        read_only_fields = ["id", "username", "role"]


class LoginSerializer(serializers.Serializer):
    """登录请求序列化器"""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
