import bs4 as BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests

from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class PressRelease(models.Model):
    url = models.URLField()
    html = models.TextField(default='')
    p_tag_text = models.TextField(default='')
    p_tag_text_char_count = models.IntegerField(default=0)
    p_tag_text_word_count = models.IntegerField(default=0)
    polarity_score = models.TextField(default='')

    def __str__(self):
        return self.url

    def save(self):
        if not self.html:
            self.html = self.get_html(self.url)
        if not self.p_tag_text:
            self.p_tag_text = self.get_p_tag_text(self.html)
        if self.p_tag_text_char_count == 0:
            self.p_tag_text_char_count = len(self.p_tag_text)
        if self.p_tag_text_word_count == 0:
            self.p_tag_text_word_count = len(self.p_tag_text.split())
        if not self.polarity_score:
            self.polarity_score = self.get_sentiment_polarity_scores(self.p_tag_text)
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

    def get_sentiment_polarity_scores(self, text):
        sid = SentimentIntensityAnalyzer()
        return sid.polarity_scores(text)
