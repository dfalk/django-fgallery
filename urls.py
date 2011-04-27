from django.conf.urls.defaults import *
from models import Photo, Album
from django.views.generic.list_detail import object_list

urlpatterns = patterns('fgallery.views',
    url(r'^$', object_list, {'queryset': Album.objects.all()}, name='gallery'),
    url(r'^add/$', 'album_add', name='album_add'),
    url(r'^(?P<album_id>\d+)/$', 'album_detail', name='gallery_one'),
    url(r'^photos/$', object_list, {'queryset': Photo.objects.all()}, name='photo_all'),
    url(r'^(?P<album_id>\d+)/upload/$', 'upload', name='gallery_upload'),
)
