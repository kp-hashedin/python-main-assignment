from django.urls import path
from . import views

urlpatterns = [
    path('label', views.create_label, name="create-label"),
    path('label/<str:label_id>', views.delete_label, name="delete-label"),
    path('issues-label/<str:label_name>', views.get_issues_as_per_label, name ='issues-label')
]