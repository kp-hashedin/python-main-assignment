from rest_framework import serializers
from .models import Issue, Project

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'
        
        extra_kwargs = {
            'reported_id': {'read_only': True},
        }
        
        
        
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        
