# -*- coding: utf-8 -*-

from django.views.generic.list_detail import object_list
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from forms import UploadAlbumForm, AddAlbumForm
from models import Photo, Album

def album_detail(request, album_id):
    queryset = Photo.objects.filter(album__id__exact=album_id)
    return object_list(request, queryset)#, {'template':'fgallery/photo_list.html'})

@login_required
def album_add(request):
    if request.method == 'POST':
        form = AddAlbumForm(request.POST)
        if form.is_valid():
             album_obj = Album()
             album_obj.author = request.user
             album_obj.title = form.cleaned_data['title']
             album_obj.slug = form.cleaned_data['slug']
             album_obj.save()
             return HttpResponseRedirect('/gallery/')
    else:
        form = AddAlbumForm()
    return direct_to_template(request, 'fgallery/album_add.html', {
        'form': form,
    })

@login_required
def album_edit(request, album_id):
    album = Album.objects.get(pk=album_id)
    if request.method == 'POST':
        form = AddAlbumForm(request.POST)
        if form.is_valid():
             album.title = form.cleaned_data['title']
             album.slug = form.cleaned_data['slug']
             album.save()
             return HttpResponseRedirect('/gallery/')
    else:
        form = AddAlbumForm({'title':album.title,'slug':album.slug})
    return direct_to_template(request, 'fgallery/album_add.html', {
        'form': form,
    })

@login_required
def album_delete(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()
    return HttpResponseRedirect('/gallery/')

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
