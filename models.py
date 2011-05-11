# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Album(models.Model):
    author = models.ForeignKey(User)
    is_published = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=datetime.now)
    date_modified = models.DateTimeField(auto_now=True)    

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

from PIL import Image
#from easy_thumbnails.files import get_thumbnailer
import os
import settings

def get_image_path(instance, filename):
    return os.path.join('gallery', str(instance.album.slug), filename)

class Photo(models.Model):
    author = models.ForeignKey(User, blank=True, null=True)
    is_published = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=datetime.now)
    date_modified = models.DateTimeField(auto_now=True)

    album = models.ForeignKey(Album, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to=get_image_path)

    is_cover = models.BooleanField(default=False)
    # TODO: js sortable
    position = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0, editable=False)
    enable_comments = models.BooleanField(default=True)
    
    def save(self, size=(1280, 1280)):
        """
        Save Photo after ensuring it is not blank.  Resize as needed.
        """
        if not self.id and not self.image:
            return

        super(Photo, self).save()

        filename = settings.MEDIA_ROOT + self.image.name
        image = Image.open(filename)
        image.thumbnail(size, Image.ANTIALIAS)
        image.save(filename, quality=90)
        #self.image = get_thumbnailer(self.image).get_thumbnail(dict(size=size))

    def rotate(self, angle=90):
        filename = settings.MEDIA_ROOT + self.image.name
        image = Image.open(filename)
        image = image.rotate(angle, expand=True)
        image.save(filename, quality=90)
