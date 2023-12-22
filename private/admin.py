from django.contrib import admin
from .models import PrivateEntry

class PrivateEntryAdmin(admin.ModelAdmin):
    readonly_fields = ( 'added_date',)

admin.site.register(PrivateEntry, PrivateEntryAdmin)
