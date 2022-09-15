from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

import backend
from .serializers import CommentSerializer

from .models import Comment
from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth import get_user_model

from backend import serializers
import sys
sys.path.append("..")
from backend.models import Issue
from logs.views import create_entry


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request):
    """
    Create comment on an issue,
    Payload - issue_id, comment, created_by
    """
    payload = {
        "comment": request.data['comment'],
        "issue_id": request.data['issue_id'],
        "commented_by": str(request.user)
    }
    
    # check whether issue exist or Not
    issue = Issue.get_issue_by_issue_id(request.data['issue_id'])
    if issue == None:
        return Response({
            "error": "Issue with given ID doesn't exists"
        }, status = status.HTTP_400_BAD_REQUEST)
    serializer = CommentSerializer(data = payload)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED)
    return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
        
@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def single_comment_operations(request, pk):
    """
    Update / Delete comment with comment_id
    """
    
    try:
        current_comment = Comment.get_comment_by_id(pk)
        if current_comment == None:
            return Response({
            "error": "comment doesn't exist"
        }, status = status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "error": "comment doesn't exist"
        }, status = status.HTTP_400_BAD_REQUEST)
    current_comment_value = current_comment.comment 
    if request.method == 'PATCH':
        if current_comment.commented_by != str(request.user):
            return Response({
                "error": "Not Allowed"
            }, status = status.HTTP_406_NOT_ACCEPTABLE)
        data = {
            "comment": request.data['comment']
        }
        serializer = CommentSerializer(current_comment, data= data, partial= True)
        if serializer.is_valid():
            serializer.save()
            
            # This payload will take care of Event Logs
            # Will make entry inside Logs Table
            payload_for_log = {
                "issue_id": current_comment.issue_id,
                "updated_field": "Comment",
                "previous_value": current_comment_value,
                "updated_value": request.data['comment']
            }
            create_entry(payload_for_log)
            
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        if current_comment.commented_by != str(request.user):
            return Response({
                "error": "Not Allowed"
            }, status = status.HTTP_406_NOT_ACCEPTABLE)
        current_comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_comments_on_issue(request, issue_id):
    """
    Retrieve comments on an existing issue
    """
    
    current_issue = Issue.get_issue_by_issue_id(issue_id)
    if current_issue == None:
        return Response(({
            "error": "No issue present"
        }), status= status.HTTP_404_NOT_FOUND)
        
    comments_on_issue = Comment.get_comments_by_issue_id(issue_id)
    if len(comments_on_issue) == 0:
        return Response({
            "resp": "No comments found for this issue"
        }, status=status.HTTP_204_NO_CONTENT)
    
    serializer = CommentSerializer(comments_on_issue, many= True) 
    return Response(serializer.data)
  
  