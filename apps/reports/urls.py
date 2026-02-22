from django.urls import path

from .views import ReportsListApiView, ReportsCreateApiView

urlpatterns = [
    # Admin (tz.json)
    path("admin/reports/", ReportsListApiView.as_view(), name="admin-reports"),
    # Tutor reports (tz.json)
    path("tutor/reports/", ReportsCreateApiView.as_view(), name="tutor-reports"),
    # Legacy
    path("reports/", ReportsListApiView.as_view(), name="report-list"),
    path("report/create/", ReportsCreateApiView.as_view(), name="report-create"),
]