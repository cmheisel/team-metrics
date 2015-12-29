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
    issue_type = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Story, bug, epic, etc.",
        null=False,
        blank=False,
    )
    queued_at = models.DateTimeField(
        null=False,
        help_text="When did the team commit to doing the work item?"
    )
    started_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When did the team start working on the item?"
    )
    ended_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When did the team complete work on the item?"
    )
    cycle_time = models.DurationField(
        null=True,
        blank=True,
        help_text="Time between ended_at and started_at"
    )
    lead_time = models.DurationField(
        null=True,
        blank=True,
        help_text="Time between ended_at and queued_at"
    )
    effort_score = models.IntegerField(
        null=True,
        blank=True,
        help_text="Story points, estimated hours, etc."
    )
    impact_score = models.IntegerField(
        null=True,
        blank=True,
        help_text="Dollar value, bug impact, etc."
    )

    class Meta:
        unique_together = ('key', 'dataset')

    def __str__(self):
        return u"{} / {}".format(self.key, self.dataset.name)
