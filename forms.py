from django import forms

class UserUploadForm(forms.Form):
    title = forms.CharField(max_length=50)
    image = forms.ImageField()
