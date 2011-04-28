from django import forms

class AddAlbumForm(forms.Form):
    title = forms.CharField(max_length=50)
    slug = forms.CharField(max_length=50)

class UploadAlbumForm(forms.Form):
    image = forms.ImageField()
