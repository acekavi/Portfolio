from django import forms
from .models import Comment
from django.utils.translation import gettext_lazy as _

# from ckeditor.widgets import CKEditorWidget

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content','parent']
        widgets = {
            'content' : forms.Textarea(attrs={'class': 'form-control rounded bg-darker text-light',
                                              'aria-label': "Comment",
                                              'aria-describedby':"comment-btn",
                                              'style': "min-height:50px;"
                                              }),
        }

class PostSearchForm(forms.Form):
    q = forms.CharField()