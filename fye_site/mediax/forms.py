# B:\desarrollo\FeyEsp2.0\fye_site\mediax\forms.py
from django import forms
from .models import MediaItem

class MediaItemForm(forms.ModelForm):
    class Meta:
        model = MediaItem
        fields = ["file", "title", "visibility"]
