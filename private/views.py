from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import PrivateEntryForm
from .models import PrivateEntry
from .functions import process_chords_text

from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect

import re
import requests as req
import json


class PrivateEntryCreationView(CreateView):
    """View for add chords page"""
    template_name = 'private/add.html'
    form_class = PrivateEntryForm
    success_url = reverse_lazy('private_entries')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.added_by = self.request.user
        instance.to_publish = True if 'publish' in self.request.POST else False
        instance.save()
        return HttpResponseRedirect(self.success_url)


class PrivateEntriesListView(LoginRequiredMixin, ListView):
    """View for my chords page"""
    template_name = 'private/list.html'
    context_object_name = 'entries'
    model = PrivateEntry

    def get_queryset(self):
        queryset = PrivateEntry.objects.filter(added_by=self.request.user).order_by('-added_date')
        return queryset


class PrivateEntryDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """View for private entry page"""
    template_name = 'private/detail.html'
    model = PrivateEntry
    context_object_name = 'entry'

    def get_object(self):
        entry = super().get_object()
        entry.text = process_chords_text(entry.text)
        return entry
    
    def get_context_data(self, **kwargs):
        """Add youtube frame and spotify link"""
        context = super().get_context_data(**kwargs)
        youtube = context['entry'].youtube
        spotify = context['entry'].spotify
        if youtube:
            resp = req.get(f"https://www.youtube.com/oembed?url={youtube}", timeout=10)
            if resp.ok:
                url = re.search(r'src="(.+)"', json.loads(resp.text)['html']).group(1).split('"')[0]
                context['youtube_frame'] = f'<iframe src="{url}"></iframe>'
        context['spotify'] = spotify
        return context

    def test_func(self):
        return self.get_object().added_by == self.request.user
