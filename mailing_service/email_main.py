import smtplib
import logging
from rest_framework import status
from dotenv import load_dotenv
import os
from django.contrib.auth import get_user_model

# Loading environment variables
load_dotenv()

User = get_user_model()
# Email server setup
server_for_email = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server_for_email.ehlo()

# Function for sending emails
def send_email(receiver_emails, email_message):
    server_for_email = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_for_email.ehlo()
    server_for_email.login(os.environ.get('SENDER_EMAIL'),os.environ.get('APP_PASSWORD'))
        
    # Since we can have many receipents, using loop
    for receiver_email in receiver_emails:
        current_user = User.objects.filter(username = receiver_email).first()
        try:
            server_for_email.sendmail(os.environ.get('SENDER_EMAIL'), current_user.email, email_message)
            logging.info("Emails sent successfully")
        except Exception as e:
            logging.error("Something went wrong")
    return status.HTTP_200_OK
        