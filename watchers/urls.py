from django.urls import path
from . import views

urlpatterns = [
    path('watcher/<int:watcher_id>', views.remove_watcher, name="delete-watcher")
]