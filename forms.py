#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from fgallery.models import Album, Photo
from fstyle.widgets import AdminImageWidget

class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ('title', 'slug')

class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ('title', 'image')
        widgets = {
            'image': AdminImageWidget(),
        }

PhotoFormSet = formset_factory(PhotoForm)
EditPhotoFormSet = inlineformset_factory(Album, Photo, form=PhotoForm, fields=('image', 'title',))
