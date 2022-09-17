from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User

from .forms import RegistrationForm, UserEditForm
from .tokens import account_activation_token
from blog.models import Post

# Create your views here.
@login_required
def profile(request):
  savedPosts = Post.postManager.filter(favorites=request.user)
  return render(request,'accounts/profile.html', {
    'section' : 'profile',
    'saved' : savedPosts,
  })

@login_required
def edit(request):
  if request.method == 'POST':
    user_form = UserEditForm(instance=request.user, data=request.POST)
    if user_form.is_valid():
      user_form.save()
      return redirect('accounts:profile')
  else:
    user_form = UserEditForm(instance=request.user)
  return render(request, 'layouts/forms.html', {
    'form': user_form,
    "title": "Edit Profile",
    "secondary": "Edit your profile here!",
    "method": "POST",
    "redirect_authenticated_user" : False,
    })


@login_required
def deleteUser(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        user.is_active = False
        user.save()
        return redirect('accounts:login')

    return render(request, 'layouts/forms.html', {
    "title": "Delete Account",
    "secondary": "It's sad to see you leave :'(",
    "method": "POST",
    "redirect_authenticated_user" : False,
    })

### Account register function
def account_register(request):
  if request.method == 'POST':
    registerForm = RegistrationForm(request.POST)

    if registerForm.is_valid():
      user = registerForm.save(commit=False)
      user.email = registerForm.cleaned_data['email']
      user.set_password(registerForm.cleaned_data['password'])
      user.is_active = False
      user.save()

      current_site = get_current_site(request)
      subject = 'Activate your account'
      message = render_to_string('layouts/activate-email.html', {
              'user': user,
              'protocol': 'http',
              'domain': current_site.domain,
              'site': 'activate/',
              'uid': urlsafe_base64_encode(force_bytes(user.pk)),
              'token': account_activation_token.make_token(user),
          })
      user.email_user(subject=subject, message=message)
      data = {
        'title' : "Registration successful",
        'context' : "Account activation link has been sent to your email. Please activate your account within 7 days. Thank you!",
      }
      return render(request, 'layouts/feedback.html', data)

  else:
      registerForm = RegistrationForm()
  
  return render(request, 'layouts/forms.html', {
    "form": registerForm,
    "title": "Register",
    "secondary": "Welcome homie!",
    "method": "POST",
    "redirect_authenticated_user" : True,
    })

### Activate account function
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('accounts:login')
    else:
      data = {
        'title' : "Activation unsuccessful",
        'context' : "This Activation link is invalid or expired.",
      }
      return render(request, 'layouts/feedback.html', data)

