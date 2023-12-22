from django.contrib import admin
from .models import Author, Song, Tuning, Capo, Strumming, PublicEntry, Comment

class PublicEntryAdmin(admin.ModelAdmin):
    readonly_fields = ( 'published_date', 'published_by')

admin.site.register(Author)
admin.site.register(Song)
admin.site.register(Tuning)
admin.site.register(Capo)
admin.site.register(Strumming)
admin.site.register(PublicEntry, PublicEntryAdmin)
admin.site.register(Comment)
