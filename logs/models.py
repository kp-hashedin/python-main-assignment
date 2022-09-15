from django.db import models

# Create your models here.

class Logs(models.Model):
    logs_id = models.AutoField(primary_key= True)
    issue_id = models.IntegerField()
    updated_field = models.CharField(max_length=20)
    time_stamp = models.DateTimeField(auto_now= True)
    previous_value = models.TextField()
    updated_value = models.TextField()
    
    @classmethod
    def get_logs_by_issue_id(cls, curr_issue_id):
        return cls.objects.filter(issue_id = curr_issue_id).all()
