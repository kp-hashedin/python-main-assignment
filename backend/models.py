from django.db import models

# Create your models here.

class Issue(models.Model):
    issue_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    desc = models.TextField()
    issue_type = models.CharField(max_length=10, default="")
    reporter_id = models.CharField(max_length=200)
    assignee_id = models.CharField(max_length=200)
    project_id = models.IntegerField()
    current_status = models.CharField(max_length=20, default="Open")

    @classmethod
    def get_issue_by_project_id(cls, proj_id):
        return cls.objects.filter(project_id = proj_id).all()
    
    @classmethod
    def get_issue_by_issue_id(cls, id):
        return cls.objects.filter(issue_id = id).first()

    

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    desc = models.TextField(default="")
    creator = models.CharField(max_length=200, default = "")
    
    @classmethod
    def get_project_by_id(cls, id):
        return cls.objects.filter(project_id = id).first()
    
    @classmethod
    def get_project_by_name(cls, proj_name):
        return cls.objects.filter(name = proj_name).first()
