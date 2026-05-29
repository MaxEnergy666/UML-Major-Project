from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/profiles/", include("profiles.urls")),
    path("api/jobs/", include("jobs.urls")),
    path("api/career/", include("career.urls")),
    path("api/admin/", include("admin_panel.urls")),
]
