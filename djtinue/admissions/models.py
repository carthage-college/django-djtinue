# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models


class LivewhaleEvents(models.Model):
    """Data model class for CMS events."""

    gid = models.IntegerField(default=settings.BRIDGE_GROUP)
    suggested = models.CharField(max_length=500, blank=True)
    parent = models.IntegerField(null=True, blank=True)
    eid = models.CharField(max_length=255, blank=True, default='')
    title = models.CharField(max_length=255)
    date_dt = models.DateTimeField(null=True, blank=True)
    date2_dt = models.DateTimeField(null=True, blank=True)
    timezone = models.CharField(max_length=255, default=settings.TIME_ZONE)
    is_all_day = models.IntegerField(null=True, blank=True)
    repeats = models.CharField(max_length=1, blank=True)
    # lw15
    repeats_from = models.DateTimeField(null=True, blank=True)
    repeats_until = models.DateTimeField(null=True, blank=True)
    # lw15
    repeats_every = models.IntegerField(null=True, blank=True)
    repeats_by = models.IntegerField(null=True, blank=True)
    repeats_on = models.CharField(max_length=15, blank=True)
    repeats_occurrences = models.IntegerField(null=True, blank=True)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=500, blank=True)
    source = models.CharField(max_length=255, blank=True)
    status = models.IntegerField(default=1)
    location = models.CharField(max_length=255, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    last_user = models.IntegerField(default=settings.BRIDGE_USER)
    created_by = models.IntegerField(
        null=True, blank=True, default=settings.BRIDGE_USER,
    )
    gallery_id = models.IntegerField(null=True, blank=True)
    has_registration = models.IntegerField(null=True, blank=True)
    is_starred = models.IntegerField(null=True, blank=True)
    has_invalid_url = models.IntegerField(null=True, blank=True)
    registration_limit = models.IntegerField(null=True, blank=True)
    # lw15
    registration_limit_each = models.IntegerField(null=True, blank=True)
    registration_instructions = models.CharField(max_length=500, blank=True)
    registration_response = models.CharField(max_length=2000, blank=True)
    has_registration_notifications = models.IntegerField(null=True, blank=True)
    registration_notifications_email = models.CharField(
        max_length=255, blank=True,
    )
    registration_restrict = models.TextField(blank=True)
    registration_owner_email = models.CharField(max_length=255, blank=True)
    has_wait_list = models.IntegerField(null=True, blank=True)
    wait_list_limit = models.IntegerField(null=True, blank=True)
    is_paid = models.IntegerField(null=True, blank=True)
    payment_price = models.CharField(max_length=11, blank=True)
    payment_method = models.IntegerField(null=True, blank=True, default=2)
    cost = models.CharField(max_length=2000, blank=True)
    is_shared = models.IntegerField(null=True, blank=True)
    views = models.IntegerField(null=True, blank=True)
    contact_info = models.CharField(max_length=1000, blank=True)
    subscription_id = models.CharField(max_length=255, blank=True)
    subscription_pid = models.IntegerField(null=True, blank=True)
    # lw15
    is_canceled = models.IntegerField(null=True, blank=True)

    class Meta:
        """Sub-class for establishing settings on the parent class."""

        managed = False
        db_table = 'livewhale_events'

    def __str__(self):
        """Default display value."""
        return self.title

    def get_absolute_url(self):
        """Return the default URL."""
        return 'https://www.carthage.edu/live/events/{0}/'.format(self.id)
