from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("profile", views.UserProfileViewSet, basename="profile")
router.register("experiences", views.ExperienceViewSet, basename="experience")
router.register("portrait", views.PortraitViewSet, basename="portrait")

urlpatterns = [
    path("", include(router.urls)),
]
