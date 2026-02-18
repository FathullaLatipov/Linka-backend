from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# from admin.views import dashboard

schema_view = get_schema_view(
    openapi.Info(
        title="Linka Mobile App API",
        default_version="v1",
        description="""
## Linka Mobile App — API for English Learning Platform

**Roles:** students and tutors

### Authorization
Most endpoints require a JWT token. After login/signup, use the `access` token in the header:
```
Authorization: Bearer <your_access_token>
```

### API Structure
- **Authentication** — registration, login, logout, token refresh
- **Student Profile** — student profile management
- **Tutors** — tutors, schedule, reviews
- **Lessons** — lessons
- **Bookings** — lesson bookings
- **Reviews** — tutor reviews
- **Reports** — complaints and reports
        """,
        contact=openapi.Contact(name="Fathulla Latipov, Oybek Zokirjonov"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # API endpoints (order affects Swagger tag grouping)
    path("api/", include("apps.users.urls")),
    path("api/", include("apps.student_profiles.urls")),
    path("api/", include("apps.tutors_profiles.urls")),
    path("api/", include("apps.lessons.urls")),
    path("api/", include("apps.bookings.urls")),
    path("api/", include("apps.reviews.urls")),
    path("api/", include("apps.reports.urls")),
    re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
