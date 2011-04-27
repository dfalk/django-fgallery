from django import forms

class AlbumForm(forms.Form):
    title = forms.CharField(max_length=50)
    slug = forms.CharField(max_length=50)

class UserUploadForm(forms.Form):
    title = forms.CharField(max_length=50)
    image = forms.ImageField()
