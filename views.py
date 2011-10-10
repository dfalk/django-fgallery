#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from fgallery.forms import AlbumForm, PhotoForm, PhotoFormSet, EditPhotoFormSet
from fgallery.models import Photo, Album

from PIL import Image as PILImage

def album_detail(request, album_id):
    queryset = Photo.objects.filter(album__id__exact=album_id)
    return object_list(request, queryset, extra_context = {'album':Album.objects.get(id=album_id)}, template_name='fgallery/album_detail.html')

@login_required
def album_edit(request, album_id=None):
    album = None
    if album_id:
        album = Album.objects.get(pk=album_id)
    if request.method == 'POST':
        forma = AlbumForm(request.POST, instance=album)
        formset = EditPhotoFormSet(request.POST, request.FILES, instance=album)
        if forma.is_valid() and formset.is_valid():
             if album == None:
                 album = Album()
                 album.author = request.user
             album.title = forma.cleaned_data['title']
             album.slug = forma.cleaned_data['slug']
             album.save()
             for form in formset.forms:
                if form.has_changed():
                    new_image = form.save(commit=False)
                    new_image.album = album
                    new_image.save()
             return HttpResponseRedirect(album.get_absolute_url())
    else:
        forma = AlbumForm(instance=album)
        formset = EditPhotoFormSet(instance=album)
    return direct_to_template(request, 'fgallery/album_new.html', {
        'forma': forma, 'formset': formset
    })

@login_required
def album_delete(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()
    # TODO: cascade operation for photos?
    return HttpResponseRedirect(reverse('gallery_index'))

def photo_detail(request, album_id, photo_id):
    queryset = Photo.objects.all()
    return object_detail(request, queryset=queryset, object_id=photo_id)

@login_required
def photo_rotate(request, album_id, photo_id, angle_opt):
    photo = Photo.objects.get(pk=photo_id)
    img = PILImage.open(photo.image)
    if angle_opt == 0:
        new_img = img.rotate(90)
    else:
        new_img = img.rotate(270)
    rotated_image = new_img.save(photo.image.file.name, overwrite=True, quality=95)
    return HttpResponseRedirect(photo.get_absolute_url())

@login_required
def album_setcover(request, album_id, photo_id):
    photo = Photo.objects.get(pk=photo_id)
    album = Photo.objects.get(pk=album_id)
    for ph in Photo.objects.filter(album=album):
        if ph.is_cover:
            ph.is_cover = False
    photo.is_cover = True
    photo.save()
    return HttpResponseRedirect(photo.get_absolute_url())
