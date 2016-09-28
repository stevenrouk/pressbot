from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import PressRelease


class IndexView(generic.ListView):
    template_name = 'articles/index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        """
        Return all of the articles in the database.
        """
        return PressRelease.objects.all()