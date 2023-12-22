from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from autoslug.fields import AutoSlugField

from PIL import Image, ImageOps, ImageSequence
from django.core.exceptions import ValidationError


def p(inst, fn):
    """Generate profile picture path"""
    return f"profile_pictures/{inst.username}_profile.{fn.split('.')[-1]}"


def file_size_validate(value):
    """Validate the size of uploaded file"""
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')


class User(AbstractUser):
    """Represents user in the system"""
    first_name = None
    last_name = None

    email = models.EmailField(_("email address"), unique=True)

    about = models.CharField(_("about"), max_length=255, blank=True)

    pfp = models.ImageField(_("profile picture"), upload_to=p, default=None, 
                            validators=[file_size_validate], null=True, blank=True)

    slug = AutoSlugField(_("user slug"), null=False, populate_from='username')

    saved = models.ManyToManyField('public.PublicEntry')

    is_moderator = models.BooleanField(
        _('moderator status'),
        default=False,
        help_text=_('Designates whether the user can moderate the entries, comments etc.'),
    )

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        """Adjust profile picture"""
        super().save(*args, **kwargs)
        if not self.pfp:
            return
        img = Image.open(self.pfp.path)
        output_size = (500, 500)
        if self.pfp.path[-4:] == '.gif':
            frames = ImageSequence.Iterator(img)
            def thumbnails(frames):
                for frame in frames:
                    thumbnail = frame.copy()
                    thumbnail = ImageOps.fit(img, output_size)
                    yield thumbnail
            frames = thumbnails(frames)
            om = next(frames)
            om.info = img.info
            om.save(self.pfp.path, save_all=True, append_images=list(frames))
        else:
            img = ImageOps.fit(img, output_size)
            img.save(self.pfp.path)
