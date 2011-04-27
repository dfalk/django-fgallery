# -*- coding: utf-8 -*-

from django.views.generic.list_detail import object_list
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response

from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from forms import UserUploadForm, AlbumForm
from models import Photo, Album

def album_detail(request, album_id):
    queryset = Photo.objects.filter(album__id__exact=album_id)
    return object_list(request, queryset)#, {'template':'fgallery/photo_list.html'})

def album_add(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
             album_obj = Album()
             album_obj.author = request.user
             album_obj.title = form.cleaned_data['title']
             album_obj.slug = form.cleaned_data['slug']
             album_obj.save()
        return HttpResponseRedirect('/gallery/')
    else:
        form = AlbumForm()
    return direct_to_template(request, 'fgallery/album_add.html', {
        'form': form,
    })

def handle_uploaded_file(f):
    destination = open(f, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def upload(request, album_id):
    if request.method == 'POST': # If the form has been submitted...
        form = UserUploadForm(request.POST, request.FILES) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            #handle_uploaded_file(request.FILES['file'])

            if request.FILES.has_key('image'):
                image_obj = Photo()
                image_obj.author = request.user
                image_obj.title = form.cleaned_data['title']
                image_obj.album = Album.objects.get(pk=album_id)
                image_obj.image.save(request.FILES['image'].name,\
                                    ContentFile(request.FILES['image'].read()))
                image_obj.save()
            return HttpResponseRedirect('/') # Redirect after POST
    else:
        form = UserUploadForm() # An unbound form

    return direct_to_template(request, 'fgallery/upload.html', {
        'form': form,
    })
