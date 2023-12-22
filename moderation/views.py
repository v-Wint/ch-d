from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django_tables2 import SingleTableView
from .tables import ModerateEntriesTable, ModerateCommentsTable

from private.forms import PrivateEntryForm
from .forms import CommentForm

from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect

from private.models import PrivateEntry
from public.models import Author, Song, Tuning, Capo, Strumming, PublicEntry, Comment


class ModerateEntriesView(LoginRequiredMixin, UserPassesTestMixin, SingleTableView):
    """View for moderate entries page"""
    table_class = ModerateEntriesTable
    queryset = PrivateEntry.objects.filter(to_publish=True).order_by('added_date')
    template_name = "moderate/entries.html"

    def test_func(self):
        return self.request.user.is_moderator or self.request.user.is_staff


class ModerateEntryView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for moderate entry page"""
    template_name = 'moderate/entry.html'
    form_class = PrivateEntryForm
    success_url = reverse_lazy('moderate_entries')
    model = PrivateEntry

    def post(self, request, *args, **kwargs):
        if 'delete' in self.request.POST:
            user_entry = PrivateEntry.objects.get(pk=self.get_object().pk)
            user_entry.to_publish = False
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # if form is valid and publish is chosen, create new public entry based on private entry information
        e = form.save(commit=False)

        if 'publish' in self.request.POST:
            author_exists = Author.objects.filter(name=e.author).exists()
            song_exists = Song.objects.filter(title=e.song).exists()
            tuning_exists = Tuning.objects.filter(title=e.tuning).exists()
            capo_exists = Capo.objects.filter(title=e.capo).exists()
            strumming_exists = Strumming.objects.filter(title=e.strumming).exists()

            if author_exists:
                author = Author.objects.get(name=e.author)
                song = Song.objects.get(title=e.song, author=author) if song_exists else Song.objects.create(title=e.song, author=author)
            else:
                author = Author.objects.create(name=e.author)
                song = Song.objects.create(title=e.song, author=author)

            if not song.youtube and e.youtube:
                song.youtube = e.youtube
            
            if not song.spotify and e.spotify:
                song.spotify = e.spotify
            song.save()

            tuning = Tuning.objects.get(title=e.tuning) if tuning_exists else Tuning.objects.create(title=e.tuning) if e.tuning else None
            capo = Capo.objects.get(title=e.capo) if capo_exists else Capo.objects.create(title=e.capo) if e.capo else None
            strumming = Strumming.objects.get(title=e.strumming) if strumming_exists else Strumming.objects.create(title=e.strumming) if e.strumming else None

            PublicEntry.objects.create(
                song = song,
                tuning = tuning,
                key = e.key,
                capo = capo,
                strumming = strumming,
                text = e.text,
                added_date = e.added_date,
                added_by = e.added_by,
                youtube = e.youtube,
                spotify = e.spotify,
                number = PublicEntry.objects.filter(song=song).count() + 1,
                published_by = self.request.user
            )

        user_entry = PrivateEntry.objects.get(pk=e.pk)
        user_entry.to_publish = False
        user_entry.save()

        return HttpResponseRedirect(self.success_url)

    def test_func(self):
        return self.request.user.is_moderator or self.request.user.is_staff


class ModerateCommentsView(LoginRequiredMixin, UserPassesTestMixin, SingleTableView):
    """View for moderate comments page"""
    table_class = ModerateCommentsTable
    queryset = Comment.objects.filter(is_moderated=False).order_by('-added_date')
    template_name = "moderate/comments.html"

    def test_func(self):
        return self.request.user.is_moderator or self.request.user.is_staff


class ModerateCommentView(UpdateView):
    """View for moderate comment page"""
    template_name = 'moderate/comment.html'
    form_class = CommentForm
    success_url = reverse_lazy('moderate_comments')
    model = Comment
    
    def form_valid(self, form):
        e = form.save(commit=False)
        if 'publish' in self.request.POST:
            e.is_moderated = True
            e.save()
        elif 'delete' in self.request.POST:
            e.delete()
        
        return HttpResponseRedirect(self.success_url)
