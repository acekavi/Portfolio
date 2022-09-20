from django import forms

class ContactForm(forms.Form):
  name = forms.CharField(max_length=255)
  subject = forms.CharField(max_length=520)
  email = forms.EmailField()
  linkedin = forms.CharField(max_length=520)
  message = forms.CharField(widget=forms.Textarea)