from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from .forms import PressReleaseURLForm
from .models import PressRelease


class IndexView(generic.ListView):
    model = PressRelease
    template_name = 'articles/index.html'
    context_object_name = 'articles'


class PressReleaseDetailView(DetailView):
    model = PressRelease


class PressReleaseCreate(CreateView):
    model = PressRelease
    fields = ['url']

    def form_valid(self, form):
        """
        If the form is valid, save the associated model and redirect to the supplied URL.
        """
        self.object = form.save()
        return HttpResponseRedirect(reverse('articles:index'))


class PressReleaseUpdate(UpdateView):
    model = PressRelease
    fields = ['url']


class PressReleaseDelete(DeleteView):
    model = PressRelease
    success_url = reverse_lazy('articles:index')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)