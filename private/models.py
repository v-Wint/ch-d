from django.db import models


class PrivateEntry(models.Model):
    """Class to represent user created not published private entries"""
    author = models.CharField(max_length=255)
    song = models.CharField(max_length=255)
    
    tuning = models.CharField(max_length=127, blank=True)
    key = models.CharField(max_length=63, blank=True)
    capo = models.CharField(max_length=127, blank=True)
    strumming = models.CharField(max_length=255, blank=True)

    text = models.TextField()

    youtube = models.URLField(max_length=511, blank=True)
    spotify = models.URLField(max_length=511, blank=True)

    added_date = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey('accounts.User', related_name='privateentry_added_set', on_delete=models.CASCADE)

    to_publish = models.BooleanField(default=False)
    number = models.PositiveSmallIntegerField(default=1)
    is_saved = models.BooleanField(default=False)

    def __str__(self):
        return self.author + ' — ' + self.song + ' ver. ' + str(self.number)
    
    class Meta:
        verbose_name = "private entry"
        verbose_name_plural = "private entries"
    
    def save(self, *args, **kwargs):
        if not PrivateEntry.objects.filter(pk=self.pk):
            self.number = PrivateEntry.objects.filter(song=self.song, author=self.author, added_by=self.added_by).count() + 1
        
        self.text = self.text.replace('\t', ' '*6)
        super().save(*args, **kwargs)
