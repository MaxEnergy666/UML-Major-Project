from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import UserProfile, Experience, MBTIResult, HollandResult, CompetencyResult
from .serializers import (
    UserProfileSerializer,
    ExperienceSerializer,
    MBTIResultSerializer,
    HollandResultSerializer,
    CompetencyResultSerializer,
    PortraitSerializer,
)


class UserProfileViewSet(viewsets.ModelViewSet):
    """用户档案视图集"""

    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExperienceViewSet(viewsets.ModelViewSet):
    """经历视图集"""

    serializer_class = ExperienceSerializer

    def get_queryset(self):
        return Experience.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PortraitViewSet(viewsets.ViewSet):
    """用户画像视图集"""

    def list(self, request):
        """获取用户画像（MBTI + 霍兰德 + 胜任力）"""
        user = request.user
        try:
            mbti = MBTIResult.objects.get(user=user)
            holland = HollandResult.objects.get(user=user)
            competency = CompetencyResult.objects.get(user=user)
        except (MBTIResult.DoesNotExist, HollandResult.DoesNotExist, CompetencyResult.DoesNotExist):
            return Response({"error": "用户画像数据不完整"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "mbti": MBTIResultSerializer(mbti).data,
            "holland": HollandResultSerializer(holland).data,
            "competency": CompetencyResultSerializer(competency).data,
        }
        return Response(data)
