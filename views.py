#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from fgallery.forms import AlbumForm, PhotoForm, PhotoFormSet, EditPhotoFormSet
from fgallery.models import Photo, Album

from PIL import Image as PILImage

def album_detail(request, album_id):
    queryset = Photo.objects.filter(album__id__exact=album_id)
    return object_list(request, queryset, extra_context = {'album':Album.objects.get(id=album_id)})#, {'template':'fgallery/photo_list.html'})

@login_required
def album_new(request):
    if request.method == 'POST':
        forma = AlbumForm(request.POST)
        formset = PhotoFormSet(request.POST, request.FILES)
        if forma.is_valid() and formset.is_valid():
             new_album = Album()
             new_album.author = request.user
             new_album.title = forma.cleaned_data['title']
             new_album.slug = forma.cleaned_data['slug']
             new_album.save()
             for form in formset.forms:
                if form.has_changed():
                    new_image = form.save(commit=False)
                    new_image.album = new_album
                    new_image.save()
             return HttpResponseRedirect(reverse('gallery_index'))
    else:
        forma = AlbumForm()
        formset = PhotoFormSet()
    return direct_to_template(request, 'fgallery/album_new.html', {
        'forma': forma, 'formset': formset
    })

@login_required
def album_edit(request, album_id):
    album = Album.objects.get(pk=album_id)
    if request.method == 'POST':
        forma = AlbumForm(request.POST, instance=album)
        formset = EditPhotoFormSet(request.POST, request.FILES, instance=album)
        if forma.is_valid() and formset.is_valid():
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
    return HttpResponseRedirect(reverse('gallery_index'))

def handle_uploaded_file(f):
    destination = open(f, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

from django.forms.formsets import formset_factory

@login_required
def album_upload(request, album_id):
    UploadFormSet = formset_factory(UploadAlbumForm, extra=5)
    if request.method == 'POST': # If the form has been submitted...
        #form = UploadAlbumForm(request.POST, request.FILES) # A form bound to the POST data
        formset = UploadFormSet(request.POST, request.FILES)
        if formset.is_valid(): # All validation rules pass
            #handle_uploaded_file(request.FILES['file'])
            for form in formset.forms:
                if form.cleaned_data:
                    image_obj = Photo()
                    image_obj.author = request.user
                    image_obj.title = form.cleaned_data['image'].name
                    image_obj.album = Album.objects.get(pk=album_id)
                    image_obj.image.save(form.cleaned_data['image'].name, ContentFile(form.cleaned_data['image'].read()))
                    image_obj.save()
            return HttpResponseRedirect('/') # Redirect after POST
    else:
        #form = UploadAlbumForm() # An unbound form
        formset = UploadFormSet()

    return direct_to_template(request, 'fgallery/album_upload.html', {
        'formset': formset,
    })

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
    return HttpResponseRedirect(photo.get_absolute_url()) # Redirect after POST
