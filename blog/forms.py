from cProfile import label
from dataclasses import field
from pyexpat import model
from unicodedata import name
from django import forms
from .models import Comment
# from ckeditor.widgets import CKEditorWidget

class NewCommentForm(forms.ModelForm):
  # content = forms.CharField(widget=CKEditorWidget())

  class Meta:
    model = Comment
    fields = ('name', 'email', 'content')
    widgets = {
      'name': forms.TextInput(attrs={'class': 'col-sm-12 form-control', 'placeholder' : "name"}),
      'email': forms.TextInput(attrs={'class': 'col-sm-12 form-control', 'placeholder' : "name@example.com"}),
      'content': forms.Textarea(attrs={'class': 'form-control', 'rows':"4", 'placeholder' : "Comment content"}),
    }


# {{ myform.media }}