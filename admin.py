#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from fgallery.models import Album, Photo

admin.site.register(Album)
admin.site.register(Photo)

