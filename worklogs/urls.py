from django.urls import path
from . import views

urlpatterns = [
    path('estimated-time-issue', views.add_estimated_time, name="estimated-issue-time"),
    path('worklog', views.add_worklog, name="add-worklog"),
    path('worklog/<int:pk>', views.singel_worklog_operations, name="single-worklog-operations")
]