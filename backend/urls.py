from urllib.parse import urlparse
from django.urls import path
from . import views

urlpatterns = [
    path('issue-list/', views.fetch_issues, name="issue-list"),
    path('create-issue/', views.create_issue, name="create-issue"),
    path('issue/<str:pk>', views.single_issue_operations, name = "issue-by-id"),
    path('issue-title/<str:pk>', views.fetch_issue_by_title, name= "issue-by-tilte"),
    path('projects-list/', views.fetch_projects, name ="fetch-projects"),
    path('create-project/', views.create_project, name="create-project"),
    path('project/<str:pk>', views.fetch_project_by_id, name="project-by-id")
]