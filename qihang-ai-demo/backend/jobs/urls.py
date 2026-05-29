from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("postings", views.JobPostingViewSet, basename="job-posting")
router.register("favorites", views.JobFavoriteViewSet, basename="job-favorite")

urlpatterns = [
    path("", include(router.urls)),
]
