from django.db import models

from djtools.fields import BINARY_CHOICES
from djforms.processors.models import Contact

from django_extensions.db.fields.encrypted import EncryptedCharField


class Course(models.Model):

    title = models.CharField(
        max_length=255
    )
    course_number = models.CharField(
        max_length=128
    )
    abstract = models.TextField()
    credits = models.IntegerField(
        max_length=2
    )
    audience = models.TextField(
        null=True, blank=True
    )
    instructors = models.CharField(
        max_length=255,
        null=True, blank=True
    )
    dates = models.TextField(
        null=True, blank=True
    )
    room = models.CharField(
        max_length=128,
        null=True, blank=True
    )
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'djtinue_enrichment_course'


class Registration(Contact):

    phone_home = models.CharField(
        verbose_name='Home phone',
        max_length=24,
        help_text="Format: XXX-XXX-XXXX",
        null=True, blank=True
    )
    phone_work = models.CharField(
        verbose_name='Work phone',
        max_length=24,
        help_text="Format: XXX-XXX-XXXX",
        null=True, blank=True
    )
    email_work = models.EmailField(
        "Work email",
        max_length=128,
        null=True, blank=True
    )
    date_of_birth = models.DateField(
        "Date of birth",
        help_text="Format: mm/dd/yyyy"
    )
    social_security_number = EncryptedCharField(
        max_length=100,
        null=True, blank=True
    )
    social_security_four = models.CharField(
        max_length=4,
        null=True, blank=True
    )
    attended_before = models.CharField(
        "Have you attended Carthage in the past?", max_length=3,
        choices=BINARY_CHOICES
    )
    collegeid = models.IntegerField(
        "College ID number",
        max_length=8,
        null=True, blank=True
    )
    verify = models.BooleanField(
        """
            I understand that courses offered and/or taken through Carthage's
            Enrichment program cannot be applied toward any undergraduate or
            graduate degree at Carthage.
        """,
        default=False
    )
    courses = models.ManyToManyField(
        Course,
        related_name="enrichment_registration_courses",
        null=True, blank=True
    )

    class Meta:
        db_table = 'djtinue_enrichment_registration'

    '''
    def order(self):
        try:
            cs = Contact.objects.filter(order=self).order_by('id')[0]
        except:
            cs = None
        return cs
    '''
