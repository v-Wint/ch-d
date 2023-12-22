from django.urls import path
from .views import HomeView, PublicEntryDetailView, AuthorEntriesView, SearchResultsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('chords/<slug:author>/<slug:song>/<int:number>', PublicEntryDetailView.as_view(), name='public_entry'),
    path('chords/<slug:slug>/', AuthorEntriesView.as_view(), name='author_entries'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
]
