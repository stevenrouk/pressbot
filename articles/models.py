import bs4 as BeautifulSoup
import datetime
import requests

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class PressRelease(models.Model):
    url = models.URLField()
    html = models.TextField(default='')
    p_tag_text = models.TextField(default='')

    def __str__(self):
        return self.url

    def save(self):
        self.html = self.get_html(self.url)
        self.p_tag_text = self.get_p_tag_text(self.html)
        super(PressRelease, self).save()

    def get_absolute_url(self):
        return reverse('press-release-detail', kwargs={'pk': self.pk})

    def get_html(self, url):
        return requests.get(url).text

    def get_p_tag_text(self, html):
        soup = BeautifulSoup.BeautifulSoup(html, 'html.parser')
        p_tags = soup.findAll('p')
        p_text = '\n'.join([tag.text for tag in p_tags])
        clean_p_text = ' '.join(p_text.split())
        return clean_p_text