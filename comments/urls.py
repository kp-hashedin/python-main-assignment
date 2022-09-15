from django.urls import path
from . import views

urlpatterns = [
    path('comment/', views.create_comment, name="create-comment"),
    path('comment/<str:pk>', views.single_comment_operations, name="comment-update-delete"),
    path('issue/comments/<str:issue_id>', views.get_comments_on_issue, name="issue-comments")
]