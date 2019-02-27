# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from djforms.core.models import GenericChoice
from djforms.processors.models import Contact
from djtools.fields import BINARY_CHOICES, GENDER_CHOICES, PAYMENT_CHOICES
from djtools.fields.helpers import upload_to_path
from djtools.fields.validators import MimetypeValidator

from django_extensions.db.fields.encrypted import EncryptedCharField

from functools import partial

#FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)
#FILE_VALIDATORS = []
FILE_VALIDATORS = [MimetypeValidator('application/pdf')]


class Application(Contact):
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
        help_text="Format: XXX-XXX-XXXX"
    )
    phone_tertiary = models.CharField(
        verbose_name='Cell phone',
        max_length=16,
        help_text="Format: XXX-XXX-XXXX"
    )
    birth_date = models.DateField(
        "Date of birth",
        help_text="Format: mm/dd/yyyy",
        blank=True, null=True
    )
    birth_place = models.CharField(
        "Place of birth",
        max_length=48, blank=True, null=True
    )
    gender = models.CharField(
        max_length=16, choices = GENDER_CHOICES
    )
    hispanic = models.CharField(
        "Are you Hispanic or Latino?",
        max_length=4, choices=BINARY_CHOICES
    )
    race = models.ManyToManyField(
        GenericChoice,
        #related_name="application_race",
        help_text = 'Check all that apply'
    )
    military = models.CharField(
        max_length=4, choices=BINARY_CHOICES
    )
    social_security_number = EncryptedCharField(
        max_length=12, null=True, blank=True
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
        max_length=4, choices=BINARY_CHOICES
    )
    cv = models.FileField(
        "Résumé",
        upload_to = partial(upload_to_path, 'admissions/CV'),
        validators=FILE_VALIDATORS,
        max_length=768,
        help_text="PDF format"
    )
    program = models.CharField(
        max_length=254, null=True, blank=True,
        default='Degree Seeking Masters Degree'
    )
    entry_term = models.CharField(max_length=4)
    entry_year = models.CharField(max_length=4)
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
    recommend_name_1 = models.CharField(
        max_length=128, blank=True, null=True
    )
    recommend_email_1 = models.CharField(
        max_length=254, blank=True, null=True
    )
    recommend_name_2 = models.CharField(
        max_length=128, blank=True, null=True
    )
    recommend_email_2 = models.CharField(
        max_length=254, blank=True, null=True
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


class Schools(models.Model):
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
        db_table = 'djtinue_admissions_schools'
