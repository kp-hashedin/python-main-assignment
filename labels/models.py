from django.db import models

# Create your models here.

class Label(models.Model):
    label_id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=50)
    issue_id = models.IntegerField()
    
    @classmethod
    def get_lable_with_label_id(cls, curr_lable_id):
        return cls.objects.filter(label_id = curr_lable_id).first()
    
    @classmethod
    def get_issues_with_label_name(cls, curr_label_name):
        return cls.objects.filter(label = curr_label_name).all()
