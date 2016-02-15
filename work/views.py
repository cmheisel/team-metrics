from rest_framework import viewsets

from .models import DataSet, WorkItem
from .serializers import DataSetSerializer, WorkItemSerializer

class DataSetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows DataSets to be viewed or edited.
    """
    queryset = DataSet.objects.all().order_by('name')
    serializer_class = DataSetSerializer

class WorkItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows WorkItems to be viewed or edited.
    """
    queryset = WorkItem.objects.all().order_by('dataset', 'key', 'queued_at')
    serializer_class = WorkItemSerializer
