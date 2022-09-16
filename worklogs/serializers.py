from rest_framework import serializers
from .models import Worklog, IssueEstimatedTime

class WorklogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worklog
        fields = '__all__'
        
class IssueEstimatedTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueEstimatedTime
        fields = '__all__'