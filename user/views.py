from django.views.generic import DetailView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
from public.models import PublicEntry
from private.models import PrivateEntry
from .forms import UpdateUserForm
from django.urls import reverse_lazy, reverse


class ProfileDetailView(DetailView):
    """View for user page"""
    model = User
    template_name = 'profile/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['entries'] = PublicEntry.objects.filter(added_by=context['object']).order_by('-published_date')
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View for user edit page"""
    model = User
    form_class = UpdateUserForm
    template_name = 'profile/edit.html'
    context_object_name = 'updated_user'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'slug': self.object.slug})

    def get(self, request, *args, **kwargs):
        self.kwargs[self.pk_url_kwarg] = self.request.user.pk
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.kwargs[self.pk_url_kwarg] = self.request.user.pk
        return super().post(request, *args, **kwargs)


class Entry:
    """Data structure to encapsulate public and published entry"""
    def __init__(self, link, title, added, is_public):
        self.link, self.title, self.added, self.is_public = link, title, added, is_public


class SavedEntriesListView(LoginRequiredMixin, TemplateView):
    """View for saved page"""
    template_name = 'profile/saved.html'

    context_object_name = 'entries'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entries = []
        for entry in PublicEntry.objects.filter(user=self.request.user):
            entries.append(Entry(
                reverse('public_entry', args=(entry.song.author.slug, entry.song.slug, entry.number,)), str(entry), entry.added_date, True))
        for entry in PrivateEntry.objects.filter(added_by = self.request.user, is_saved=True):
            entries.append(Entry(reverse('private_entry', args=(entry.pk, )), str(entry), entry.added_date, False))

        entries.sort(key=lambda x: x.title)
        context['entries'] = entries
        return context
