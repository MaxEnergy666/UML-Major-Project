from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("users", views.AdminUserViewSet, basename="admin-user")
router.register("logs", views.SystemLogViewSet, basename="system-log")
router.register("stats", views.StatsViewSet, basename="stats")

urlpatterns = [
    path("", include(router.urls)),
]
