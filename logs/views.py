from rest_framework import status
from rest_framework.response import Response
from .serializers import LogsSerializer

# Adding entry into Logs Table
# Do not need to create API, 
# This function will create Log, whenever called

def create_entry(payload):
    log_entry = LogsSerializer(data = payload)
    if log_entry.is_valid():
        log_entry.save()
        return Response(log_entry.data)
    return Response(log_entry.errors, status = status.HTTP_400_BAD_REQUEST)
       