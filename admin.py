#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from fgallery.models import Album, Photo

class AlbumAdmin(admin.ModelAdmin):
    date_hierarchy = "publish"
    list_per_page = 20
    list_display = ["title", "publish", "is_published"]
    list_editable = ["is_published"]
    actions = ["make_published"]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

    def make_published(self, request, queryset):
        queryset.update(is_published=True)
    make_published.short_description = "Mark selected entries as published"

admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, AlbumAdmin)

