from django.urls import path
from .views import (SaveEntryView, CheckDbView, AddCommentView,
                    AuthorsAutocompleteView, SongsAutocompleteView, CaposAutocompleteView, 
                    StrummingsAutocompleteView, TuningsAutocompleteView)

urlpatterns = [
    path('save/', SaveEntryView.as_view(), name='api_save'),
    path('autocomplete/authors/', AuthorsAutocompleteView.as_view(), name='authors_autocomplete'),
    path('autocomplete/songs/', SongsAutocompleteView.as_view(), name='songs_autocomplete'),
    path('autocomplete/tunings/', TuningsAutocompleteView.as_view(), name='tunings_autocomplete'),
    path('autocomplete/capos/', CaposAutocompleteView.as_view(), name='capos_autocomplete'),
    path('autocomplete/strummings/', StrummingsAutocompleteView.as_view(), name='strummings_autocomplete'),
    path('check/', CheckDbView.as_view(), name='check_db'),
    path('comment/add/', AddCommentView.as_view(), name='add_comment')
]
