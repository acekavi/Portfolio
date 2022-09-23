from django import forms
from . import models

class ContactForm(forms.Form):
  name = forms.CharField(max_length=255)
  subject = forms.CharField(max_length=520)
  email = forms.EmailField()
  linkedin = forms.CharField(max_length=520)
  message = forms.CharField(widget=forms.Textarea)

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = models.ArtComment
        fields = ['content','parent']
        widgets = {
            'content' : forms.Textarea(attrs={'class': 'form-control rounded bg-darker text-light',
                                              'aria-label': "Comment",
                                              'aria-describedby':"comment-btn",
                                              'style': "min-height:50px;"
                                              }),
        }