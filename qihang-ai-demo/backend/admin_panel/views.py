from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import User
from career.models import MockInterviewRecord, ResumeOptimizationReport
from jobs.models import JobPosting
from .models import SystemLog
from .serializers import AdminUserSerializer, SystemLogSerializer, StatsSerializer


class AdminUserViewSet(viewsets.ReadOnlyModelViewSet):
    """管理员用户视图集"""

    queryset = User.objects.all()
    serializer_class = AdminUserSerializer


class SystemLogViewSet(viewsets.ReadOnlyModelViewSet):
    """系统日志视图集"""

    queryset = SystemLog.objects.all()
    serializer_class = SystemLogSerializer


class StatsViewSet(viewsets.ViewSet):
    """统计数据视图集"""

    def list(self, request):
        data = {
            "total_users": User.objects.count(),
            "active_users": User.objects.filter(is_active=True).count(),
            "verified_users": User.objects.filter(is_verified=True).count(),
            "total_interviews": MockInterviewRecord.objects.count(),
            "total_resume_reports": ResumeOptimizationReport.objects.count(),
            "total_job_postings": JobPosting.objects.count(),
        }
        return Response(data)
