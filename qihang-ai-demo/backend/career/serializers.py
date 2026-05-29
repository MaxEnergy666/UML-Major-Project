from rest_framework import serializers
from .models import (
    CareerPlanReport,
    CareerDirection,
    JobRecommendation,
    ImprovementSuggestion,
    MockInterviewRecord,
    InterviewMessage,
    ResumeOptimizationReport,
)
from jobs.serializers import JobPostingSerializer


class CareerPlanReportSerializer(serializers.ModelSerializer):
    """职业规划报告序列化器"""

    class Meta:
        model = CareerPlanReport
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class CareerDirectionSerializer(serializers.ModelSerializer):
    """就业方向序列化器"""

    class Meta:
        model = CareerDirection
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at"]


class JobRecommendationSerializer(serializers.ModelSerializer):
    """岗位推荐序列化器"""

    job = JobPostingSerializer(read_only=True)

    class Meta:
        model = JobRecommendation
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at"]


class ImprovementSuggestionSerializer(serializers.ModelSerializer):
    """提升建议序列化器"""

    class Meta:
        model = ImprovementSuggestion
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at"]


class InterviewMessageSerializer(serializers.ModelSerializer):
    """面试消息序列化器"""

    class Meta:
        model = InterviewMessage
        fields = "__all__"
        read_only_fields = ["id", "interview", "created_at"]


class MockInterviewRecordSerializer(serializers.ModelSerializer):
    """模拟面试记录序列化器"""

    messages = InterviewMessageSerializer(many=True, read_only=True)

    class Meta:
        model = MockInterviewRecord
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at", "completed_at"]


class ResumeOptimizationReportSerializer(serializers.ModelSerializer):
    """简历优化报告序列化器"""

    class Meta:
        model = ResumeOptimizationReport
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at"]


class InterviewConfigSerializer(serializers.Serializer):
    """面试配置序列化器"""

    target_job = serializers.CharField(required=True)
    interview_type = serializers.ChoiceField(choices=MockInterviewRecord.TYPE_CHOICES, required=True)
    rounds = serializers.IntegerField(min_value=1, max_value=10, default=3)
