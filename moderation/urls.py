from django.urls import path
from .views import ModerateEntriesView, ModerateEntryView, ModerateCommentsView, ModerateCommentView


urlpatterns = [
    path('', ModerateEntriesView.as_view(), name='moderate_entries'),
    path('<int:pk>', ModerateEntryView.as_view(), name='moderate_entry'),
    path('comments/', ModerateCommentsView.as_view(), name='moderate_comments'),
    path('comments/<int:pk>', ModerateCommentView.as_view(), name='moderate_comment')
]
