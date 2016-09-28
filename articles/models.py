import datetime

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class PressRelease(models.Model):
    release_url = models.URLField()

    def __str__(self):
        return self.release_url