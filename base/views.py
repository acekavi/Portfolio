from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.views.generic.base import TemplateView
from .forms import ContactForm
from django.contrib import messages

### Projects views
class ProjectDetails(TemplateView):

    template_name = "base/test.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['value'] = "1111111111111"
        return context

class ProjectsView(TemplateView):

    template_name = "base/test.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

### Designs views
class DesignsView(TemplateView):

    template_name = "base/designs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['home_page'] = "active"
        return context

class DesignDetails(TemplateView):

    template_name = "base/designs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['value'] = "2222222222222"
        return context

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