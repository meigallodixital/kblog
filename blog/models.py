from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.timezone import now


class Post(models.Model):
    """
    Post Model
    Define the attributes of a post
    title, slug must be unique
    slug is the search key
    """
    title = models.CharField(max_length=250, unique=True,)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    body = models.TextField()
    image = models.ImageField(upload_to='blog/%Y/%m/%d', blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    published_at = models.DateTimeField(default=now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Create slug if not exists
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
