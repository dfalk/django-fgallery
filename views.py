# -*- coding: utf-8 -*-

from django.views.generic.list_detail import object_list
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response

from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from forms import UserUploadForm
from models import Photo

def handle_uploaded_file(f):
    destination = open(f, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def upload(request):
    if request.method == 'POST': # If the form has been submitted...
        form = UserUploadForm(request.POST, request.FILES) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            #handle_uploaded_file(request.FILES['file'])

            if request.FILES.has_key('image'):
                image_obj = Photo()
                image_obj.author = request.user
                image_obj.title = form.cleaned_data['title']
                image_obj.image.save(request.FILES['image'].name,\
                                    ContentFile(request.FILES['image'].read()))
                image_obj.save()
            return HttpResponseRedirect('/') # Redirect after POST
    else:
        form = UserUploadForm() # An unbound form

    return direct_to_template(request, 'fgallery/upload.html', {
        'form': form,
    })
