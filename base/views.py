from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.views.generic.base import TemplateView
from .forms import ContactForm, NewCommentForm
from . import models
from django.contrib import messages
from django.views.generic import DetailView,ListView

from django.shortcuts import get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

### Projects views
def projectDetails(request, slug):

    template_name = f"projects/{slug}.html"
    filteredProject = models.Project.projectManager.filter(slug = slug).first()

    return render(request, template_name, {
        'project': filteredProject,
    })

class ProjectsView(ListView):

    template_name = "base/projects.html"
    model= models.Project
    context_object_name ='projects'
    paginate_by = 6
    queryset = models.Project.projectManager.all().order_by('publish').reverse()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

### Designs views
class DesignsView(ListView):
    template_name = "designs/designs.html"
    model= models.Artwork
    context_object_name ='designs'
    paginate_by = 12
    queryset = models.Artwork.objects.all().order_by('publish').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['home_page'] = "active"
        return context

class DesignDetails(DetailView):
    template_name= 'designs/artwork-details.html'
    model= models.Artwork
    context_object_name= 'design'

    def get_context_data(self, **kwargs):
            data = super().get_context_data(**kwargs)

            filteredDesign = models.Artwork.objects.filter(slug = self.kwargs.get('slug')).first()
            comments = models.ArtComment.objects.filter(artwork = filteredDesign)

            data['design'] = filteredDesign
            data['comments'] = comments
            data['comment_form'] = NewCommentForm()
            return data

    def post(self , request , *args , **kwargs):
        if self.request.method == 'POST':
            comment_form = NewCommentForm(self.request.POST)
            if comment_form.is_valid():
                content = comment_form.cleaned_data['content']
                try:
                    parent = comment_form.cleaned_data['parent']
                except:
                    parent=None

            new_comment = models.ArtComment(content=content , author = self.request.user , post=self.get_object() , parent=parent)
            new_comment.save()
            return redirect(self.request.path_info)

@login_required
def designLike(request, id):
    design = get_object_or_404(models.Artwork, id=id)
    if request.user in design.likes.all():
        design.likes.remove(request.user)
    else:
        design.likes.add(request.user)
    return HttpResponseRedirect(reverse('base:designs-details', kwargs={ 'slug': design.slug }))


###### Home page
def indexView(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            linkedin = form.cleaned_data['linkedin']
            message = form.cleaned_data['message']

            html = render_to_string('layouts/contact-email.html', {
                'name': name,
                'subject': subject,
                'email': email,
                'linkedin':linkedin,
                'message': message
            })

            send_mail(subject, message, email, ['acekavi.me@gmail.com'], html_message=html)
            messages.success(request, 'Contact request submitted successfully.')
            return redirect('base:homepage')
        else:
            messages.error(request, 'Contact request failed!')
            return redirect('base:homepage')
    else:
        form = ContactForm()
        messages.error(request, form.errors)

    return render(request, "base/home.html", {
        'form': form
    })