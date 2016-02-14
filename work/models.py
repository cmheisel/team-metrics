from django.db import models
from django.utils.text import slugify

SLUG_LENGTH = 75


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
        max_length=SLUG_LENGTH,
        unique=True,
        db_index=True,
    )

    def clean_fields(self, *args, **kwargs):
        if not self.slug and self.name:
            slug = slugify(self.name)
            if len(slug) > SLUG_LENGTH:
                slug = slug[0:SLUG_LENGTH]
            self.slug = slug
        super(DataSet, self).clean_fields(*args, **kwargs)

    def __str__(self):
        return self.name


class WorkItem(models.Model):
    """
    Data about a story, defect, epic, etc.
    """
    # Required fields
    dataset = models.ForeignKey(
        DataSet,
        on_delete=models.CASCADE
    )
    key = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Unique reference to the item in your ticket tracker (JIRA Key, Story number, etc.)"
    )
    queued_at = models.DateTimeField(
        null=False,
        blank=False,
        help_text="When did the team commit to doing the work item?"
    )

    # Optional fields
    issue_type = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Story, bug, epic, etc.",
        null=True,
        blank=True,
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

    # Computed fields
    _cycle_time = models.DurationField(
        null=True,
        blank=True,
        db_column="cycle_time",
        help_text="Time between ended_at and started_at"
    )
    _lead_time = models.DurationField(
        null=True,
        blank=True,
        db_column="lead_time",
        help_text="Time between ended_at and queued_at"
    )
    _week_queued_at = models.DateField(
        null=True,
        blank=True,
        help_text="The Sunday of the week the team committed to doing the work item?"
    )
    _week_started_at = models.DateField(
        null=True,
        blank=True,
        help_text="The Sunday of the week the team start working on the item"
    )
    _week_ended_at = models.DateField(
        null=True,
        blank=True,
        help_text="The Sunday of the week the team compelted working on the item"
    )

    class Meta:
        unique_together = ('key', 'dataset')

    def __str__(self):
        return u"{} / {}".format(self.dataset.name, self.key)
