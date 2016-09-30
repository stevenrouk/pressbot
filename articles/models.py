import datetime

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class PressRelease(models.Model):
    url = models.URLField()

    def __str__(self):
        return self.url

    def get_absolute_url(self):
        return reverse('press-release-detail', kwargs={'pk': self.pk})