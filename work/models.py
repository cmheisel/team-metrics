from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from .services.calculations import sunday_of_week

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

    def save(self, *args, **kwargs):
        self.full_clean()
        super(DataSet, self).save(*args, **kwargs)

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

    @property
    def cycle_time(self):
        if self.ended_at and self.started_at:
            return self.ended_at - self.started_at
        return None

    @property
    def lead_time(self):
        if self.ended_at and self.queued_at:
            return self.ended_at - self.queued_at
        return None

    @property
    def is_in_progress(self):
        if self.started_at and not self.ended_at:
            return True
        return False

    @property
    def is_completed(self):
        if self.started_at and self.ended_at:
            return True
        return False

    @property
    def week_queued_at(self):
        return sunday_of_week(self.queued_at)

    @property
    def week_started_at(self):
        if self.started_at:
            return sunday_of_week(self.started_at)
        return None

    @property
    def week_ended_at(self):
        if self.ended_at:
            return sunday_of_week(self.ended_at)
        return None

    def check_dates(self):
        if self.started_at:
            if self.started_at < self.queued_at:
                raise ValidationError({'started_at': "Work on an item must start at/after it is queued."})
        if self.ended_at:
            if self.ended_at < self.queued_at:
                raise ValidationError({'ended_at': "Work on an item must end at/after it is queued."})
            if self.ended_at < self.started_at:
                raise ValidationError({'ended_at': "Work on an item must end at/after it is started."})

    def clean(self):
        self.check_dates()
        if self.is_completed:
            self._cycle_time = self.cycle_time
            self._lead_time = self.lead_time

        self._week_queued_at = self.week_queued_at
        self._week_started_at = self.week_started_at
        self._week_ended_at = self.week_ended_at

    def save(self, *args, **kwargs):
        self.full_clean()
        super(WorkItem, self).save(*args, **kwargs)

    def __str__(self):
        return u"{} / {}".format(self.dataset.name, self.key)
