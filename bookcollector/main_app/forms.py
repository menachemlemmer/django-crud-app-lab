from django import forms
from .models import Book, Bookmark


class BookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ["name", "page"]
        labels = {
            "name": "Bookmark Name",
            "page": "Page Number",
        }
