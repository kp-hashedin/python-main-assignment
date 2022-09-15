from xmlrpc.client import ResponseError
from django.shortcuts import render
from functools import partial
from django.shortcuts import render
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

import backend
from backend import serializers
from .serializers import LabelSerializer

from .models import Label
from rest_framework.permissions import IsAuthenticated
import sys
sys.path.append("..")
from backend.models import Issue

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_label(request):
    """
    Create label on an issue
    """
    current_issue = Issue.get_issue_by_issue_id(request.data['issue_id'])
    if current_issue == None:
        return ResponseError({
            "resp": "Issue with given id doesn't exist"
        }, status=status.HTTP_400_BAD_REQUEST)
    serializer = LabelSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response({
        "error": "Something went wrong",
    })
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_label(request, label_id):
    """
    Delete label from issue
    """
    try: 
        current_label = Label.get_lable_with_label_id(label_id)
        current_label.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({
            "Error": "Something went Wrong.."
        }, status = status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_issues_as_per_label(request, label_name):
    """
    Fetch issues that lied in a label
    """
    issues_id = Label.get_issues_with_label_name(label_name)
    if len(issues_id) == 0:
        return Response({
            "error": "Issue not Present"
        }, status = status.HTTP_400_BAD_REQUEST)
    
    list_of_issues = []
    for issue_id in issues_id:
        current_issue = Issue.get_issue_by_issue_id(issue_id.issue_id)
        serializer = serializers.IssueSerializer(current_issue)
        list_of_issues.append(serializer.data)
    return Response({
        "resp": list_of_issues
    }, status= status.HTTP_200_OK)
        
        