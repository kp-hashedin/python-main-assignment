from django.db import models

# Create your models here.

class Watcher(models.Model):
    watcher_id = models.AutoField(primary_key= True)
    issue_id = models.IntegerField()
    user_id = models.CharField(max_length=60)
    
    @classmethod
    def get_watcher_by_issue_id(cls, curr_issue_id):
        return cls.objects.filter(issue_id = curr_issue_id).all()

    @classmethod
    def get_watcher_by_id(cls, curr_watcher_id):
        return cls.objects.filter(watcher_id = curr_watcher_id).first()