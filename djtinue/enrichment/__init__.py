from django.conf import settings

if settings.DEBUG:
    TO_LIST = [settings.ADMINS[0][1],]
else:
    TO_LIST = [
        settings.CONTINUING_STUDIES_ENRICHMENT_REGISTRATION_EMAIL,
        settings.ADMINS[0][1]
    ]
BCC = settings.MANAGERS
