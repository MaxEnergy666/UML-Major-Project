from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import JobPosting, JobFavorite
from .serializers import JobPostingSerializer, JobFavoriteSerializer


class JobPostingViewSet(viewsets.ReadOnlyModelViewSet):
    """岗位视图集（只读）"""

    serializer_class = JobPostingSerializer

    def get_queryset(self):
        queryset = JobPosting.objects.filter(is_active=True)

        # 筛选条件
        city = self.request.query_params.get("city")
        job_type = self.request.query_params.get("job_type")
        salary_min = self.request.query_params.get("salary_min")
        salary_max = self.request.query_params.get("salary_max")
        keyword = self.request.query_params.get("keyword")

        if city:
            queryset = queryset.filter(city=city)
        if job_type:
            queryset = queryset.filter(job_type=job_type)
        if salary_min:
            queryset = queryset.filter(salary_max__gte=int(salary_min))
        if salary_max:
            queryset = queryset.filter(salary_min__lte=int(salary_max))
        if keyword:
            queryset = queryset.filter(title__icontains=keyword) | queryset.filter(company__icontains=keyword)

        return queryset

    @action(detail=True, methods=["post"])
    def favorite(self, request, pk=None):
        """收藏/取消收藏岗位"""
        job = self.get_object()
        user = request.user

        fav, created = JobFavorite.objects.get_or_create(user=user, job=job)
        if not created:
            fav.delete()
            return Response({"is_favorited": False})
        return Response({"is_favorited": True})


class JobFavoriteViewSet(viewsets.ModelViewSet):
    """收藏视图集"""

    serializer_class = JobFavoriteSerializer

    def get_queryset(self):
        return JobFavorite.objects.filter(user=self.request.user)
