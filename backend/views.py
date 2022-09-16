from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from logs.serializers import LogsSerializer
from logs.views import create_entry
from watchers.models import Watcher
from watchers.views import create_watcher
from .serializers import IssueSerializer, ProjectSerializer

from .models import Issue, Project
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from backend import serializers
import sys
sys.path.append('..')
from logs.models import Logs
from logs.serializers import LogsSerializer
from mailing_service.email_main import send_email

User = get_user_model()


# Issue's Status List
issues_status_list = ["Open", "In Progress", "In Review", "Code Complete", "Done"]

def get_possible_status(current_status):
    if current_status == "Open":
        return ["In Progress"]
    elif current_status == "In Progress":
        return ["Open", "In Review"]
    elif current_status == "In Review":
        return ["Open", "Code Complete"]
    elif current_status == "Code Complete":
        return ["Open", "Done"]
    else:
        return []
    
    
# Issue's alterable fields
issues_alterable_fields = ["title", "desc", "issue_type", "assignee_id", "current_status"]

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_issue_status(request, id):
    """
    Update status of an issue
    Open -> InProgress -> In Review -> Code Complete -> Done
    Follow Sequentially, or Open
    """
    current_issue = Issue.get_issue_by_issue_id(id)
    possible_status = get_possible_status(current_issue.current_status)
    
    if request.data['updated_status'] in possible_status:
        data = {
            "current_status": request.data['updated_status']
        }
        serializer = IssueSerializer(current_issue, data = data, partial= True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
    return Response({
        "error": "Allowed status are" + str(possible_status)
    }, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    

# Issue API's
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_issues(request):
    """
    Retrieving all issues present inside backend-issue Table
    """
    issues = Issue.objects.all()
    serializers = IssueSerializer(issues, many = True)
    return Response(serializers.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_issue(request):
    """
    Create New issue by passing
    title, desc, assignee_id, project_name_or_id and issue_type
    reporter_id will taken automatically from current user
    """
    request.data['reporter_id'] = str(request.user)
    payload = {
        "title": request.data['title'],
        "desc": request.data['desc'],
        "reporter_id": str(request.user),
        "assignee_id": request.data['assignee_id'],
        "issue_type": request.data['issue_type'],
    }
    
    if type(request.data['project_id_or_project_name']) == str:
        proj_id = Project.get_project_by_name(request.data['project_id_or_project_name'])
        if proj_id == None:
            return Response({
                "error":"project doesn't exist, make sure you use correct id or name."
            }, status = status.HTTP_406_NOT_ACCEPTABLE)
        payload['project_id'] = proj_id.project_id
    else:
        payload['project_id'] = request.data['project_id_or_project_name']

    serializer = IssueSerializer(data=payload)
    if serializer.is_valid():
        
        # Check for Project exist or Not
        check = Project.get_project_by_id(payload['project_id'])
        # Check for assignee_exist or Not
        check_for_assignee = User.objects.filter(username = request.data['assignee_id'])
        if check == None or len(check_for_assignee) == 0:
            return Response({"error":"project or user doesn't exist"}, status = status.HTTP_406_NOT_ACCEPTABLE)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def single_issue_operations(request, pk):
    """
    Retrieve, update and delete operation on issue
    """
    try:
        issue = Issue.objects.get(issue_id = pk)
    except Exception as e:
        return Response({
            'error': 'Issue does not exist'
        }, status = status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = IssueSerializer(instance= issue, many=False)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = IssueSerializer(issue, data= request.data)
        if serializer.is_valid():
            if issue.reporter_id == request.data['reporter_id']:
                
                # Added entry into Logs
                issue_dict = vars(issue)
                
                list_of_updated_fields = []
                for field in issues_alterable_fields:
                    if issue_dict[field] != request.data[field]:
                        list_of_updated_fields.append(field)
                        payload_for_logs ={
                            "issue_id": pk,
                            "updated_field": field,
                            "previous_value":issue_dict[field],
                            "updated_value": request.data[field]
                        }
                        create_entry(payload_for_logs)
                message = "Hii, " +str(list_of_updated_fields) + " has been updated"  
                watchers = Watcher.get_watcher_by_issue_id(pk)
                lis_of_watchers = set()
                for watcher in watchers:
                    lis_of_watchers.add(watcher.user_id)
                lis_of_watchers.add(issue.assignee_id) #Assignee will be default watcher
                lis_of_watchers.add(issue.reporter_id) #Repoter will be default watcher
                serializer.save()
                send_email(lis_of_watchers, message)
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response({
                "error": "Reporter of Issue can not be chnaged"
            }, status= status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    else:
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_issue_by_title(request, pk):
    """
    Retrieve issue by title
    """
    issues = Issue.objects.filter(title = pk).all()
    serializer = IssueSerializer(instance= issues, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_issue_log(request, issue_id):
    """
    Retrive logs of an existing issue
    """
    logs = Logs.get_logs_by_issue_id(issue_id)
    serializer = LogsSerializer(logs, many=True)
    return Response({
        "response": serializer.data
    }, status = status.HTTP_201_CREATED)
        
        
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def add_watcher(request, issue_id):
    try:
        issue = Issue.get_issue_by_issue_id(issue_id)
    except Exception as e:
        return Response({
            'error': 'Issue does not exist'
        }, status = status.HTTP_400_BAD_REQUEST)
    if request.method == 'POST':
        payload_for_watcher = {
            "issue_id": issue_id,
            "user_id": request.data['username']
        }
        
        resp = create_watcher(payload_for_watcher)
        if resp.status_code == 201:
            return Response({
                "message": "Watcher added successfully"
            }, status= status.HTTP_201_CREATED )
        else:
            return Response({
                "error": "Something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        watchers = Watcher.get_watcher_by_issue_id(issue_id)
        issue = Issue.get_issue_by_issue_id(issue_id)
        lis_of_watchers = set()
        for watcher in watchers:
            lis_of_watchers.add(watcher.user_id)
        lis_of_watchers.add(issue.assignee_id) # Assignee will be default watcher
        lis_of_watchers.add(issue.reporter_id) #Reporter will be default watcher
        return Response({
            "resp": lis_of_watchers
        }, status= status.HTTP_200_OK)
        
        
    
# Project API's
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_projects(request):
    """
    Retrieve Projects along with subsequent issues and details
    """
    projects = Project.objects.all()
    serializers = ProjectSerializer(projects, many= True)
    resp = {}
    try:
        for proj in projects:
            issues = Issue.get_issue_by_project_id(proj.project_id)
            resp[proj.name] = list(issues.values())
            
        return Response({
            "response": resp
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({"error":"Something went wrong.."}, status = status.HTTP_404_NOT_FOUND)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_project(request):
    """
    Create Project project_name, creator, description
    """
    request.data['creator'] = str(request.user)
    serializer = ProjectSerializer(data = request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_project_by_id(request, pk):
    """
    Retrieve single project with details like, project desc and name
    """
    try:
        project = Project.objects.get(project_id = pk)
        serializer = ProjectSerializer(instance= project, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error":"Something went wrong.."}, status = status.HTTP_404_NOT_FOUND)
