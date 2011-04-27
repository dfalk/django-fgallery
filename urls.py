from django.conf.urls.defaults import *
from models import Photo
from django.views.generic.list_detail import object_list

urlpatterns = patterns('',
    url(r'^$', object_list, {'queryset': Photo.objects.all()}),
    url(r'^upload/$', 'fgallery.views.upload', name='gallery_upload'),
)
