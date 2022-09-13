from urllib import request
from django import forms
from django.contrib.auth.models import User

## Registration form
class RegistrationForm(forms.ModelForm):
  username=forms.CharField( min_length=4, max_length=50)
  email=forms.EmailField(max_length=100, error_messages={
    'required': "Please provide a valid email address",
  })
  password = forms.CharField(widget=forms.PasswordInput)
  password2 = forms.CharField(widget=forms.PasswordInput , label='Confirm Password:')

  class Meta:
    model = User
    fields = ( 'username', 'email', 'first_name')

  def clean_username(self):
    enteredUsername = self.cleaned_data['username'].lower()
    r = User.objects.filter(username=enteredUsername)

    if r.count():
      raise forms.ValidationError("Username already exists!")
    return enteredUsername

  def clean_password2(self):
    pwd1 = self.cleaned_data['password']
    pwd2 = self.cleaned_data['password2']
    if pwd1 != pwd2:
      raise forms.ValidationError('Passwords do not match!')
    return pwd2

  def clean_email(self):
    email = self.cleaned_data['email']
    if User.objects.filter(email=email).exists():
      raise forms.ValidationError('This email is already registered!')
    return email


## User edit form
class UserEditForm(forms.ModelForm):
  username = forms.CharField(
    label='Username:', min_length=4, max_length=50, widget=forms.TextInput(
      attrs={'class': 'active',}
    ))

  first_name = forms.CharField(
    label='First name:', min_length=4, max_length=50, widget=forms.TextInput(
      attrs={'class': 'active',}
    ))
          
  last_name = forms.CharField(
    label='Last name:', min_length=4, max_length=50, widget=forms.TextInput(
      attrs={'class': 'active',}
    ))

  email = forms.EmailField(
    label='Email:',max_length=200, widget=forms.TextInput(
      attrs={'class': 'active',}
    ))

  class Meta:
    model = User
    fields = ('username','first_name', 'last_name', 'email')

  def clean_email(self):
    email = self.cleaned_data['email']
    currentEmail = self.instance.email
    if email != currentEmail and User.objects.filter(email=email).exists():
        raise forms.ValidationError(
            'This email is already taken!')
    return email

  def clean_username(self):
      username = self.cleaned_data['username']
      currentUsername = self.instance.username
      if username != currentUsername and User.objects.filter(username=username).exists():
          raise forms.ValidationError(
              'This username is already taken!')
      return username
      
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].required = False
    self.fields['first_name'].required = False
    self.fields['last_name'].required = False
    self.fields['email'].required = False