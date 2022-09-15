from django.db import models
from datetime import datetime

# Create your models here.

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    issue_id = models.IntegerField()
    comment = models.CharField(max_length=200)
    commented_by = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    
    @classmethod
    def get_comment_by_id(cls, curr_comment_id):
        return cls.objects.filter(comment_id  = curr_comment_id).first()
    
    @classmethod
    def get_comments_by_issue_id(cls, curr_issue_id):
        return cls.objects.filter(issue_id = curr_issue_id).all()
    
    
