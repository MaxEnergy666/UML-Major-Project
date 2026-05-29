from rest_framework import serializers
from .models import JobPosting, JobFavorite


class JobPostingSerializer(serializers.ModelSerializer):
    """岗位序列化器"""

    salary_range = serializers.ReadOnlyField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = JobPosting
        fields = "__all__"

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return JobFavorite.objects.filter(user=request.user, job=obj).exists()
        return False


class JobFavoriteSerializer(serializers.ModelSerializer):
    """收藏序列化器"""

    job = JobPostingSerializer(read_only=True)

    class Meta:
        model = JobFavorite
        fields = ["id", "job", "created_at"]
        read_only_fields = ["id", "user", "created_at"]
