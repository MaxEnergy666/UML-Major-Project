from rest_framework import serializers
from .models import UserProfile, Experience, MBTIResult, HollandResult, CompetencyResult


class ExperienceSerializer(serializers.ModelSerializer):
    """经历序列化器"""

    class Meta:
        model = Experience
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at"]


class UserProfileSerializer(serializers.ModelSerializer):
    """用户档案序列化器"""

    experiences = ExperienceSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class MBTIResultSerializer(serializers.ModelSerializer):
    """MBTI 结果序列化器"""

    class Meta:
        model = MBTIResult
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at"]


class HollandResultSerializer(serializers.ModelSerializer):
    """霍兰德结果序列化器"""

    class Meta:
        model = HollandResult
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at"]


class CompetencyResultSerializer(serializers.ModelSerializer):
    """胜任力结果序列化器"""

    class Meta:
        model = CompetencyResult
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at"]


class PortraitSerializer(serializers.Serializer):
    """用户画像完整序列化器"""

    mbti = MBTIResultSerializer()
    holland = HollandResultSerializer()
    competency = CompetencyResultSerializer()
