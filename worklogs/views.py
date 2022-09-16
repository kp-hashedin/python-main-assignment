from math import perm
from os import stat
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

import backend
from backend import serializers
from .serializers import WorklogSerializer, IssueEstimatedTimeSerializer

from .models import Worklog, IssueEstimatedTime
from rest_framework.permissions import IsAuthenticated


# API for Estimated issue time
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_estimated_time(request):
    serializer = IssueEstimatedTimeSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED)
    return Response({
        "error": "Something went wrong"
    }, status = status.HTTP_400_BAD_REQUEST)
    

# APIs for worklogs with user_id
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_worklog(request):
    payload = {
        "issue_id": request.data['issue_id'],
        "user_id": str(request.user),
        "logged_time": request.data['logged_time']
    }
    #check whether estimated time exist or not
    estimated_time_entry = IssueEstimatedTime.get_estimated_time_by_id(request.data['issue_id'])
    if estimated_time_entry == None:
        payload['estimated_time'] = None
    else:
        payload['estimated_time'] = estimated_time_entry.estimated_time
        
    serializer = WorklogSerializer(data = payload)
    print("######################")
    print(payload)
    print("#################################")
    if serializer.is_valid():
        serializer.save()
        return Response(payload, status=status.HTTP_201_CREATED)
    return Response({"error": "something went wrong"}, status = status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def singel_worklog_operations(request, pk):
    """
    Update/ Delete worklog with worklog_id
    """
    current_worklog = Worklog.get_worklog_by_id(pk)
    if current_worklog == None:
        return Response({
            "error": "Worklog doesn't exist"
        }, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'PATCH':
        estimated_time_entry = IssueEstimatedTime.get_estimated_time_by_id(current_worklog.issue_id)
        payload = {
            "logged_time": request.data['logged_time']
        }
        if estimated_time_entry == None:
            payload['estimated_time'] = None
        else:
            payload['estimated_time'] = estimated_time_entry.estimated_time
        serializer = WorklogSerializer(current_worklog, data = payload, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "worklog updated successfully"
            }, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        current_worklog.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    
    else:
        return Response({
            "message": "Method Not Allowed"
        }, status = status.HTTP_405_METHOD_NOT_ALLOWED)