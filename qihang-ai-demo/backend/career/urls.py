from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("plans", views.CareerPlanViewSet, basename="career-plan")
router.register("directions", views.CareerDirectionViewSet, basename="career-direction")
router.register("recommendations", views.JobRecommendationViewSet, basename="job-recommendation")
router.register("improvements", views.ImprovementSuggestionViewSet, basename="improvement")
router.register("interviews", views.MockInterviewViewSet, basename="mock-interview")
router.register("resume", views.ResumeOptimizationViewSet, basename="resume-optimization")

urlpatterns = [
    path("", include(router.urls)),
]
