from django.conf import settings

if settings.DEBUG:
    TO_LIST = [settings.SERVER_EMAIL,]
else:
    TO_LIST = [settings.GPS_ENRICHMENT_REGISTRATION_EMAIL,]
BCC = settings.MANAGERS
