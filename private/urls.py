from django.urls import path
from .views import PrivateEntryCreationView, PrivateEntriesListView, PrivateEntryDetailView


urlpatterns = [
    path('add/', PrivateEntryCreationView.as_view(), name='add'),
    path('my-chords/', PrivateEntriesListView.as_view(), name='private_entries'),
    path('my-chords/<int:pk>', PrivateEntryDetailView.as_view(), name='private_entry')
]
