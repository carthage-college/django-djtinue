# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connections
from django.utils.timezone import utc
from django.utils.html import escape

from djtools.utils.users import in_group
#from djtools.templatetags.text_mungers import convert_smart_quotes

import datetime

# dictionary name corresponds to URL slug
STYPES = {
    "information-session":712,
    "graduate-studies":715,
    "undergraduate-studies":713,
    "master-social-work":714,
    "paralegal":582
}

class LivewhaleEvents(models.Model):
    gid = models.IntegerField(default=settings.BRIDGE_GROUP)
    suggested = models.CharField(max_length=500, blank=True)
    parent = models.IntegerField(null=True, blank=True)
    eid = models.CharField(max_length=255, blank=True, default="")
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
    created_by = models.IntegerField(null=True, blank=True, default=settings.BRIDGE_USER)
    lookup = models.CharField(max_length=255, blank=True)
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
    registration_notifications_email = models.CharField(max_length=255, blank=True)
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
        db_table = u'livewhale_events'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "http://www.carthage.edu/live/events/%s/" % self.id

    def tag(self, jid=None):
        return get_tag(self.id,jid)

    def save(self, data=None, *args, **kwargs):
        self.title.encode('latin1')
        self.summary.encode('latin1')
        self.description.encode('latin1')
        #self.title = convert_smart_quotes(self.title)
        #self.summary = convert_smart_quotes(self.summary)
        #self.description = convert_smart_quotes(self.description)
        if data:
            u = data["user"]
            # date munging
            if data['start_time']:
                self.date_dt = datetime.datetime.combine(data['start_date'],data['start_time'])
            else:
                self.date_dt = data['start_date']
            if data['end_time']:
                self.date2_dt = datetime.datetime.combine(data['end_date'],data['end_time'])
            else:
                self.date2_dt = data['end_date']
            # set contact info from request.user
            self.contact_info = '<p>By:&nbsp;<a href="mailto:%s">%s %s</a></p>' % (
                u.email, u.first_name,
                u.last_name
            )
            if in_group(u, "Staff", "Faculty"):
                self.status = 1
            else: # student
                self.status = 0
        # save
        super(LivewhaleEvents, self).save(*args, **kwargs)
        """
        We have to resort to raw sql since Django does not support
        composite Foreign Keys
        """
        if data:
            # tag
            sql = """
                INSERT INTO livewhale_tags2any
                    (id1, id2, type)
                VALUES
                    ('%s', '%s', 'events')
            """ % (data["category"],self.id)
            cursor = connections['livewhale'].cursor()
            cursor.execute(sql)
            # category
            sql = """
                INSERT INTO livewhale_events_categories2any
                    (id1, id2, type)
                VALUES
                    ('%s', '%s', 'events')
            """ % (30,self.id)
            cursor.execute(sql)

class LivewhaleEvents2Any(models.Model):
    id1 = models.IntegerField()
    id2 = models.IntegerField()
    type = models.CharField(max_length=765, primary_key=True)
    position = models.IntegerField()
    class Meta:
        db_table = u'livewhale_events2any'

class LivewhaleEventsCategories(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=765)
    is_starred = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'livewhale_events_categories'

class LivewhaleEventsCategories2Any(models.Model):
    id1 = models.IntegerField()
    id2 = models.IntegerField()
    type = models.CharField(max_length=765, primary_key=True)
    class Meta:
        db_table = u'livewhale_events_categories2any'

class LivewhaleEventsRegistrations(models.Model):
    id = models.IntegerField(primary_key=True)
    pid = models.IntegerField()
    firstname = models.CharField(max_length=765)
    lastname = models.CharField(max_length=765)
    email = models.CharField(max_length=765, blank=True)
    phone = models.CharField(max_length=765, blank=True)
    attending = models.IntegerField(null=True, blank=True)
    comments = models.CharField(max_length=1500, blank=True)
    is_cancelled = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'livewhale_events_registrations'

class LivewhaleEventsSubscriptions(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField()
    title = models.CharField(max_length=765)
    url = models.CharField(max_length=1500)
    description = models.CharField(max_length=1500, blank=True)
    last_refreshed = models.DateTimeField()
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(null=True, blank=True)
    status = models.IntegerField()
    use_external = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'livewhale_events_subscriptions'

class LivewhaleTags(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=765)
    is_starred = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = u'livewhale_tags'

    def __unicode__(self):
        return self.title

class LivewhaleTags2Any(models.Model):
    id1 = models.IntegerField()
    id2 = models.IntegerField()
    type = models.CharField(max_length=765, primary_key=True)

    class Meta:
        db_table = u'livewhale_tags2any'
