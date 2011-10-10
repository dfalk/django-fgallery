#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from fgallery.models import Photo, Album
from django.views.generic.list_detail import object_list, object_detail

urlpatterns = patterns('fgallery.views',
    url(r'^$', object_list, {'queryset': Album.objects.all()}, name='gallery_index'),

    url(r'^new/$', 'album_edit', name='album_new'),
    url(r'^(?P<album_id>\d+)/$', 'album_detail', name='album_detail'),
    url(r'^(?P<album_id>\d+)/edit/$', 'album_edit', name='album_edit'),
    url(r'^(?P<album_id>\d+)/delete/$', 'album_delete', name='album_delete'),

    url(r'^(?P<album_id>\d+)/(?P<photo_id>\d+)/$', 'photo_detail', name='photo_detail'),
    url(r'^(?P<album_id>\d+)/(?P<photo_id>\d+)/setcover/$', 'album_setcover', name='album_setcover'),
    url(r'^(?P<album_id>\d+)/(?P<photo_id>\d+)/rotate/(?P<angle_opt>[0-1])', 'photo_rotate', name='photo_rotate'),

)
