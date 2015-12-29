from django.db import models


class DataSet(models.Model):
    """
    Serves as a collection for :model:`work.WorkItem`
    """
    name = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=75,
    )

    def __str__(self):
        return self.name


class WorkItem(models.Model):
    """
    Data about a story, defect, epic, etc.
    """
    dataset = models.ForeignKey(
        DataSet,
        on_delete=models.CASCADE
    )
    key = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Reference to the item in your ticket tracker (JIRA Key, Story number, etc.)"
    )

    class Meta:
        unique_together = ('key', 'dataset')

    def __str__(self):
        return u"{} / {}".format(self.key, self.dataset.name)
