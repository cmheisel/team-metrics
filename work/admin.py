from django.contrib import admin

from .models import (
    DataSet,
    WorkItem,
)


@admin.register(DataSet)
class DataSetAdmin(admin.ModelAdmin):
    list_display = ('name', )


def dataset_name(obj):
    return obj.dataset.name


@admin.register(WorkItem)
class WorkItemAdmin(admin.ModelAdmin):
    list_display = (dataset_name, 'key')
