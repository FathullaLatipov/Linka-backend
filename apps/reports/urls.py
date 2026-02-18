from django.urls import path

from .views import ReportsListApiView, ReportsCreateApiView

urlpatterns = [
    path("reports/", ReportsListApiView.as_view(), name="report-list"),
    path("report/create", ReportsCreateApiView.as_view(), name="report-create"),

]