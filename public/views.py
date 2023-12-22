from django.views.generic import DetailView, TemplateView, ListView

from .models import PublicEntry, Author, Song
from .functions import process_chords_text

import json
import requests as req
import re


class HomeView(TemplateView):
    """View for home page"""
    template_name = 'home.html'


class PublicEntryDetailView(DetailView):
    """View for public entry page"""
    template_name = 'public/detail.html'
    model = PublicEntry
    context_object_name = 'entry'

    def get_object(self):
        d = self.kwargs
        author = Author.objects.get(slug=d['author'])
        song = Song.objects.get(slug=d['song'], author=author)

        obj = PublicEntry.objects.get(song=song, number=d['number'])

        obj.text = process_chords_text(obj.text)
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entry_added'] = self.get_object().user_set.filter(pk=self.request.user.pk).exists()
        youtube = context['entry'].youtube if context['entry'].youtube else context['entry'].song.youtube
        spotify = context['entry'].spotify if context['entry'].spotify else context['entry'].song.spotify
        if youtube:
            resp = req.get(f"https://www.youtube.com/oembed?url={youtube}", timeout=10)
            if resp.ok:
                url = re.search(r'src="(.+)"', json.loads(resp.text)['html']).group(1).split('"')[0]
                context['youtube_frame'] = f'<iframe src="{url}"></iframe>'
        context['spotify'] = spotify
        return context


class AuthorEntriesView(ListView):
    """View for author page"""
    template_name = 'public/author.html'
    model = Song
    context_object_name = 'songs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = Author.objects.get(slug=self.kwargs['slug'])
        return context
    
    def get_queryset(self):
        return self.model.objects.filter(author=Author.objects.get(slug=self.kwargs['slug']))


class SearchResultsView(TemplateView):
    """View for search results page"""
    template_name = "public/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        songs = list(Song.objects.filter(title__icontains=self.request.GET.get("q")))
        authors = list(Author.objects.filter(name__icontains=self.request.GET.get("q")))
        songs += list(Song.objects.filter(author__in=authors))
        context['songs'] = list(set(songs))
        context['authors'] = authors[:5]
        return context
