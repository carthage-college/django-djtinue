# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from djforms.core.models import GenericChoice
from djforms.core.models import GenericContact
from djforms.processors.models import Contact as ApplicationContact
from djtools.fields import BINARY_CHOICES
from djtools.fields import GENDER_CHOICES
from djtools.fields.helpers import upload_to_path
from djtools.fields.validators import MimetypeValidator
from encrypted_model_fields.fields import EncryptedCharField


FILE_VALIDATORS = [MimetypeValidator('application/pdf')]
PAYMENT_CHOICES = (
    ('Credit Card', 'Credit Card'),
    ('Check', 'Check'),
    ('Cash/Money Order', 'Cash/Money Order'),
    ('Waiver Code', 'Waiver Code'),
)
TIMELINE_CHOICES = (
    (
        'One-year program (10 months intensive)',
        'One-year program (10 months intensive)',
    ),
    (
        'Multi-year program (typically two years)',
        'Multi-year program (typically two years)',
    ),
)
TRACK_CHOICES = (
    (
        'Master of Music: Music Theatre Vocal Pedagogy',
        'Master of Music: Music Theatre Vocal Pedagogy',
    ),
    (
        'Master of Music: Music Pedagogy',
        'Master of Music: Music Pedagogy',
    ),
)


class Application(ApplicationContact):
    """Data class model for admissions application."""

    updated_by = models.ForeignKey(
        User,
        verbose_name='Updated by',
        editable=False,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    slug = models.CharField(
        max_length=64,
        default='generic',
        blank=True,
        null=True,
    )
    viewed = models.BooleanField(default=False)
    # contact information
    phone_secondary = models.CharField(
        verbose_name='Phone 2',
        max_length=16,
        null=True,
        blank=True,
    )
    phone_tertiary = models.CharField(
        verbose_name='Phone 3',
        max_length=16,
        null=True,
        blank=True,
    )
    # personal information
    birth_date = models.DateField(
        'Date of birth',
        help_text='Format: mm/dd/yyyy',
    )
    birth_place = models.CharField(
        'Place of birth',
        help_text='City, State/Provence, Country',
        max_length=48,
        blank=True,
        null=True,
    )
    gender = models.CharField(
        max_length=16,
        choices=GENDER_CHOICES,
    )
    latinx = models.CharField(
        'Are you Hispanic or Latinx',
        max_length=4,
        choices=BINARY_CHOICES,
        blank=True,
        null=True,
    )
    race = models.ManyToManyField(
        GenericChoice,
        help_text='Check all that apply',
        blank=True,
    )
    social_security_number = EncryptedCharField(
        max_length=254, null=True, blank=True,
    )
    social_security_four = models.CharField(
        max_length=4, null=True, blank=True,
    )
    program = models.CharField(
        max_length=254,
        default='Degree Seeking Masters Degree',
        null=True,
        blank=True,
    )
    entry_term = models.CharField(
        default='RA', max_length=4, blank=True, null=True,
    )
    entry_month = models.CharField(
        max_length=4, blank=True, null=True,
    )
    entry_year = models.CharField(max_length=4)
    track = models.CharField(
        'Which track in Master of Music are you interested in pursuing?',
        max_length=64,
        choices=TRACK_CHOICES,
        blank=True,
        null=True,
    )
    instrument = models.CharField(
        'Principal performing instrument',
        max_length=64,
        blank=True,
        null=True,
    )
    timeline = models.CharField(
        'Which program timeline are you applying for?',
        max_length=64,
        choices=TIMELINE_CHOICES,
        blank=True,
        null=True,
    )
    fellowships = models.CharField(
        'Are you interested in being considered for a Graduate Assistantship?',
        max_length=4,
        choices=BINARY_CHOICES,
    )
    scholarships = models.CharField(
        'Are you interested in being considered for Carthage scholarships?',
        max_length=4,
        choices=BINARY_CHOICES,
    )
    housing = models.CharField(
        'Are you interested in Carthage graduate housing?',
        max_length=4,
        choices=BINARY_CHOICES,
    )
    # employment information
    employer = models.CharField(max_length=128, null=True, blank=True)
    position = models.CharField(max_length=128, null=True, blank=True)
    tuition_reimbursement = models.CharField(
        'Does your employer offer tuition reimbursement?',
        max_length=4,
        choices=BINARY_CHOICES,
        null=True,
        blank=True,
    )
    military = models.CharField(
        'Have you ever served in the military?',
        max_length=4,
        choices=BINARY_CHOICES,
    )
    cv = models.FileField(
        'Résumé',
        upload_to=upload_to_path,
        validators=FILE_VALIDATORS,
        help_text='PDF format',
        max_length=768,
        null=True,
        blank=True,
    )
    # educational information
    # privacy GDPR waiver
    gdpr = models.CharField(
        verbose_name="""Are you currently located in a European Union country,
            Iceland, Liechtenstein, Norway, or Switzerland?
        """,
        max_length=3,
        choices=BINARY_CHOICES,
    )
    gdpr_cookies = models.BooleanField(default=False)
    gdpr_transfer = models.BooleanField(default=False)
    gdpr_collection = models.BooleanField(default=False)
    # audition information
    audition_date = models.ForeignKey(
        GenericChoice,
        verbose_name='Audition Date',
        related_name='audition_date',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    audition_time = models.ForeignKey(
        GenericChoice,
        verbose_name='Audition Time',
        related_name='audition_time',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    # payment
    payment_method = models.CharField(choices=PAYMENT_CHOICES, max_length=24)
    payment_waiver = models.CharField(
        'Payment waiver code',
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        """Sub-class for settings about the parent class."""

        verbose_name = 'Submissions'
        verbose_name_plural = 'Submissions'
        db_table = 'djtinue_admissions_application'

    def get_slug(self):
        """Return the slug for file uploads."""
        return 'files/admissions/application/'

    def get_race(self):
        """Obtain all of the races."""
        race = ''
        for raza in self.race.all():
            race += '{0}, '.format(raza)
        return race[:-1]


class School(models.Model):
    """Generic institutions of education."""

    application = models.ForeignKey(
        Application,
        related_name='schools',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(
        'State/Provence',
        max_length=50,
        blank=True,
        null=True,
    )
    degree = models.CharField(
        'Diploma/Degree',
        max_length=255,
        blank=True,
        null=True,
    )
    attended = models.CharField(
        'Dates Attended',
        max_length=255,
        blank=True,
        null=True,
    )
    majorminor = models.CharField(
        'Major(s)/Minor(s)',
        max_length=255,
        blank=True,
        null=True,
    )
    gpa = models.DecimalField(
        'GPA',
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
    )
    transcript = models.FileField(
        'Transcript (can be unofficial) in PDF',
        upload_to=upload_to_path,
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True,
        blank=True,
        help_text="""
            Transcripts may be submitted after you submit your
            application for admission. Application will not be
            reviewed until transcripts are received.
        """,
    )

    class Meta:
        """Sub-class for settings about the parent class."""

        db_table = 'djtinue_admissions_school'

    def get_slug(self):
        """Return the slug path for file uploads."""
        return 'files/admissions/school/'

    def __str__(self):
        """Display the default value."""
        return '{0}'.format(self.name)


class Contact(GenericContact):
    """Generic contact for things like recommendations."""

    application = models.ForeignKey(
        Application,
        related_name='contacts',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Sub-class for settings about the parent class."""

        db_table = 'djtinue_admissions_contact'
