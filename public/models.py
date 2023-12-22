from django.db import models
from autoslug.fields import AutoSlugField


class Author(models.Model):
    """Class to represent entry song author"""
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(unique=True, populate_from='name')

    def __str__(self):
        return self.name


class Song(models.Model):
    """Class to represent entry song"""
    title = models.CharField(max_length=255)
    slug = AutoSlugField(unique_with='author', populate_from='title')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    youtube = models.URLField(max_length=512, blank=True)
    spotify = models.URLField(max_length=511, blank=True)

    def __str__(self):
        return self.author.name + ' — ' + self.title
    

class Strumming(models.Model):
    """Class to represent entry strumming"""
    title = models.CharField(max_length=255, unique = True)

    def __str__(self):
        return self.title


class Tuning(models.Model):
    """Class to represent entry tuning"""
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class Capo(models.Model):
    """Class to represent entry capo"""
    title = models.CharField(max_length=127, unique=True)

    def __str__(self):
        return self.title


class PublicEntry(models.Model):
    """Class to represent published entry"""
    song = models.ForeignKey(Song, on_delete = models.CASCADE)

    tuning = models.ForeignKey(Tuning, on_delete=models.SET_NULL, null=True, blank=True)
    key = models.CharField(max_length=127, blank=True)
    capo = models.ForeignKey(Capo, on_delete=models.SET_NULL, null=True, blank=True)
    strumming = models.ForeignKey(Strumming, on_delete=models.SET_NULL, null=True, blank=True)
    
    text = models.TextField()

    youtube = models.URLField(max_length=512, blank=True)
    spotify = models.URLField(max_length=511, blank=True)

    added_date = models.DateTimeField()
    added_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE)

    published_date = models.DateTimeField(auto_now_add=True)
    published_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='public_entry_moderator_set', null=True)

    number = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.song.__str__() + ' ver. ' + str(self.number)

    class Meta:
        verbose_name = 'public entry'
        verbose_name_plural = 'public entries'
    
    def save(self, *args, **kwargs):
        if not PublicEntry.objects.filter(pk=self.pk):
            self.number = PublicEntry.objects.filter(song=self.song).count() + 1
        
        self.text = self.text.replace('\t', ' '*6)
        super().save(*args, **kwargs)


class Comment(models.Model):
    """Class to represent public entry comment"""
    entry = models.ForeignKey(PublicEntry, on_delete=models.CASCADE)
    body = models.CharField(max_length=1024)
    added_date = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    is_moderated = models.BooleanField(default=False)
    
    def __str__(self):
        return self.added_by.username + " — " + self.body
