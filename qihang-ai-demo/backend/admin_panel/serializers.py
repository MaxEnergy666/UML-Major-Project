from rest_framework import serializers
from accounts.models import User
from .models import SystemLog


class AdminUserSerializer(serializers.ModelSerializer):
    """管理员查看用户序列化器"""

    class Meta:
        model = User
        fields = ["id", "username", "phone", "name", "role", "is_verified", "is_active", "date_joined"]


class SystemLogSerializer(serializers.ModelSerializer):
    """系统日志序列化器"""

    class Meta:
        model = SystemLog
        fields = "__all__"


class StatsSerializer(serializers.Serializer):
    """统计数据序列化器"""

    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    verified_users = serializers.IntegerField()
    total_interviews = serializers.IntegerField()
    total_resume_reports = serializers.IntegerField()
    total_job_postings = serializers.IntegerField()
