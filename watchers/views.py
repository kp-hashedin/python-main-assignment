from rest_framework import status
from rest_framework.response import Response
from backend import serializers
from watchers.models import Watcher
from watchers.serializer import WatcherSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.

def create_watcher(payload):
    watcher_entry = WatcherSerializer(data = payload)
    if watcher_entry.is_valid():
        watcher_entry.save()
        return Response(watcher_entry.data, status = status.HTTP_201_CREATED)
    return Response(watcher_entry.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_watcher(request, watcher_id):
    watcher = Watcher.get_watcher_by_id(watcher_id)
    watcher.delete()
    return Response(status= status.HTTP_204_NO_CONTENT)
    