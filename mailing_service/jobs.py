from django.conf import settings
import sys
sys.path.append('..')

from backend.models import Issue
from django.contrib.auth import get_user_model
from .email_main import send_email
import logging


User = get_user_model()


def schedule_emails():
    
    ## ALL issues with open status
    issues_list = Issue.get_issue_by_status(curr_status="Open")
    
    
    # Mapping issues with assigneing, Sending all issues into a single email to assignee's
    issue_assignee_map = {}
    for rec in issues_list:
        if rec.assignee_id in issue_assignee_map:
            temp = issue_assignee_map[rec.assignee_id]
            temp.append(vars(rec))
            issue_assignee_map[rec.assignee_id] = temp
        else:
            issue_assignee_map[rec.assignee_id] = [vars(rec)]

    
    for receiver_email, email_msg in issue_assignee_map.items():
        temp = []
        temp.append(receiver_email)
        
        #Need to work on
        formatter_msg = "Open Issues"
        
        send_email(temp, formatter_msg)
        logging.info("Emails sent successfully")
