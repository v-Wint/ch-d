from django.urls import path
from .views import ProfileDetailView, ProfileUpdateView, SavedEntriesListView

urlpatterns = [
    path('users/<slug:slug>/', ProfileDetailView.as_view(), name='profile'),
    path('user/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('saved/', SavedEntriesListView.as_view(), name='saved')
]
