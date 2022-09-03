from dataclasses import field
from pyexpat import model
from django import forms
from .models import Comment
from ckeditor.widgets import CKEditorWidget

class NewCommentForm(forms.ModelForm):
  content = forms.CharField(widget=CKEditorWidget())

  class Meta:
    model = Comment
    fields = ('name', 'email', 'content')
    widgets = {
      'name': forms.TextInput(attrs={'class': 'col-sm-12'}),
      'email': forms.TextInput(attrs={'class': 'col-sm-12'}),
      'content': forms.Textarea(attrs={'class': 'form-control', 'rows':"2"}),
    }


# {{ myform.media }}