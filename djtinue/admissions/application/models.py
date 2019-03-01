# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from djforms.core.models import GenericChoice, GenericContact
from djforms.processors.models import Contact as ApplicationContact
from djtools.fields import BINARY_CHOICES, GENDER_CHOICES, PAYMENT_CHOICES
from djtools.fields.helpers import upload_to_path
from djtools.fields.validators import MimetypeValidator

from django_extensions.db.fields.encrypted import EncryptedCharField

from functools import partial

#FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)
#FILE_VALIDATORS = []
FILE_VALIDATORS = [MimetypeValidator('application/pdf')]


class Application(ApplicationContact):
    # meta
    updated_by = models.ForeignKey(
        User,
        verbose_name="Updated by",
        #related_name='application_updated_by',
        editable=False,
        null=True, blank=True
    )
    slug = models.SlugField(unique=True)
    viewed = models.IntegerField()
    # core
    phone_secondary = models.CharField(
        verbose_name='Work phone',
        max_length=16,
    )
    phone_tertiary = models.CharField(
        verbose_name='Cell phone',
        max_length=16,
    )
    birth_date = models.DateField(
        "Date of birth",
        help_text="Format: mm/dd/yyyy",
        blank=True, null=True
    )
    birth_place = models.CharField(
        "Place of birth",
        help_text="City, State, County",
        max_length=48, blank=True, null=True
    )
    gender = models.CharField(
        max_length=16, choices = GENDER_CHOICES
    )
    latinx = models.CharField(
        "Are you Hispanic or Latinx",
        max_length=4, choices=BINARY_CHOICES
    )
    race = models.ManyToManyField(
        GenericChoice,
        #related_name="application_race",
        help_text = 'Check all that apply'
    )
    social_security_number = EncryptedCharField(
        max_length=16, null=True, blank=True
    )
    social_security_four = models.CharField(
        max_length=4, null=True, blank=True
    )
    # third party data
    employer = models.CharField(
        max_length=128, null=True, blank=True
    )
    position = models.CharField(
        max_length=128, null=True, blank=True
    )
    tuition_reimbursement = models.CharField(
        "Does your employer offer tuition reimbursement?",
        max_length=4, choices=BINARY_CHOICES,
        null=True, blank=True
    )
    military = models.CharField(
        "Have you ever served in the military?",
        max_length=4, choices=BINARY_CHOICES
    )
    cv = models.FileField(
        "Résumé",
        upload_to = partial(upload_to_path, 'admissions/CV'),
        validators=FILE_VALIDATORS,
        help_text="PDF format",
        max_length=768, null=True, blank=True
    )
    program = models.CharField(
        max_length=254, null=True, blank=True,
        default='Degree Seeking Masters Degree'
    )
    entry_term = models.CharField(default='RA', max_length=4)
    entry_month = models.CharField(
        max_length=4,
        blank=True, null=True
    )
    entry_year = models.CharField(max_length=4)
    fellowships = models.CharField(
        "Do you intend to apply for fellowships and/or assistantships?",
        max_length=4, choices=BINARY_CHOICES
    )
    gmat = models.CharField(
        max_length=4, choices=BINARY_CHOICES
    )
    gmat_date = models.DateField(
        blank=True, null=True
    )
    gmat_score = models.CharField(
        max_length=10, blank=True, null=True
    )
    gre = models.CharField(
        max_length=4, choices=BINARY_CHOICES
    )
    gre_date = models.DateField(
        blank=True, null=True
    )
    gre_score = models.CharField(
        max_length=10, blank=True, null=True
    )
    personal_statement = models.TextField(
        blank=True, null=True
    )
    # privacy GDPR waiver
    gdpr = models.CharField(
        """
            Are you currently located in a European Union country,
            Iceland, Liechtenstein, Norway, or Switzerland?
        """, max_length=3, choices=BINARY_CHOICES
    )
    gdpr_cookies = models.BooleanField(default=False)
    gdpr_transfer = models.BooleanField(default=False)
    gdpr_collection = models.BooleanField(default=False)
    # payment
    payment_method = models.CharField(
        choices=PAYMENT_CHOICES, max_length=24
    )

    class Meta:
        verbose_name = 'Submissions'
        verbose_name_plural = 'Submissions'
        db_table = 'djtinue_admissions_application'


class School(models.Model):
    """
    generic institutions of education
    """
    application = models.ForeignKey(Application)
    name = models.CharField(
        max_length=255, blank=True, null=True,
        default=''
    )
    state = models.CharField(
        max_length=50, blank=True, null=True
    )
    degree = models.CharField(
        max_length=255, blank=True, null=True
    )
    attended = models.CharField(
        max_length=255, blank=True, null=True
    )
    majorminor = models.CharField(
        max_length=255, blank=True, null=True
    )
    gpa = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True
    )
    transcript = models.FileField(
        upload_to = partial(upload_to_path, 'admissions/transcript'),
        validators=FILE_VALIDATORS,
        max_length=768,
        help_text="PDF format"
    )

    class Meta:
        db_table = 'djtinue_admissions_school'


class Contact(GenericContact):
    """
    generic contact for things like recommendations
    """
    application = models.ForeignKey(Application)

    class Meta:
        db_table = 'djtinue_admissions_contact'
