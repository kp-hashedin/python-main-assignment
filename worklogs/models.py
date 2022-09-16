from django.db import models

# Create your models here.

class Worklog(models.Model):
    worklog_id = models.AutoField(primary_key= True)
    issue_id = models.IntegerField()
    user_id = models.CharField(max_length=50)
    estimated_time = models.IntegerField(null=True, blank=True)
    logged_time = models.IntegerField()
    
    @classmethod
    def get_worklog_by_id(cls, curr_worklog_id):
        return cls.objects.filter(worklog_id = curr_worklog_id).first()
    

class IssueEstimatedTime(models.Model):
    issue_estimated_time_id = models.AutoField(primary_key= True)
    issue_id = models.IntegerField()
    estimated_time = models.IntegerField()
    
    @classmethod
    def get_estimated_time_by_id(cls, curr_issue_id):
        return cls.objects.filter(issue_id = curr_issue_id).get()
    