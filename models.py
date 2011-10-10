#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from PIL import Image
import os
import settings

class Album(models.Model):
    author = models.ForeignKey(User)

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True)

    is_published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(default=datetime.now)
    enable_comments = models.BooleanField(default=True)

    @models.permalink
    def get_absolute_url(self):
        return ('album_detail',[self.id])

def get_image_path(instance, filename):
    return os.path.join('gallery', unicode(instance.album.slug), filename)

class Photo(models.Model):
    author = models.ForeignKey(User, blank=True, null=True)

    album = models.ForeignKey(Album, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to=get_image_path)
    description = models.TextField(blank=True)

    is_cover = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=0)

    is_published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(default=datetime.now)
    enable_comments = models.BooleanField(default=True)

    def save(self, size=(1280, 1280)):
        if not self.id and not self.image:
            return

        super(Photo, self).save()

        filename = settings.MEDIA_ROOT + self.image.name
        image = Image.open(filename)
        image.thumbnail(size, Image.ANTIALIAS)
        image.save(filename, quality=95)
        #self.image = get_thumbnailer(self.image).get_thumbnail(dict(size=size))

    @models.permalink
    def get_absolute_url(self):
        return ('photo_detail',[self.album.id,self.id])

    """
    def rotate(self, angle=90):
        filename = settings.MEDIA_ROOT + self.image.name
        image = Image.open(filename)
        image = image.rotate(angle)
        image.save(filename, quality=95)
    """
