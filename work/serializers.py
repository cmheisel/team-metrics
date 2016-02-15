from rest_framework import serializers

from .models import DataSet, WorkItem

class DataSetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DataSet
        fields = ('name', 'slug')


class WorkItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WorkItem
        fields = (
            'dataset',
            'key',
            'queued_at',
            'issue_type',
            'started_at',
            'ended_at',
            'effort_score',
            'impact_score',
        )
