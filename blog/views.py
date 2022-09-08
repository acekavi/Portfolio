from turtle import pos
from unittest import result
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from .forms import NewCommentForm, PostSearchForm
from .models import Category, Post, Comment

from django.views.generic import ListView

# Create your views here.
def blogList(request):
    all_posts = Post.postManager.all()

    return render(request, 'blog/index.html', {
        'posts' : all_posts,
        'navBlog' : True,
    })

class BlogDetail(DetailView):
    template_name= 'blog/details.html'
    model= Post
    context_object_name= 'post'

    def get_context_data(self , **kwargs):
        data = super().get_context_data(**kwargs)

        filteredPost = Post.objects.filter(slug = self.kwargs.get('slug')).first()
        comments = Comment.objects.filter(post = filteredPost)

        data['post'] = filteredPost
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

            new_comment = Comment(content=content , author = self.request.user , post=self.get_object() , parent=parent)
            new_comment.save()
            return redirect(self.request.path_info)

class CategoryListView(ListView):
    template_name = 'blog/category.html'
    context_object_name = 'catList'

    def get_queryset(self):
        content = {
            'cat': self.kwargs['slug'],
            'posts': Post.objects.filter(category__name=self.kwargs['slug']).filter(status='published'),
            'navBlog' : True,
        }
        return content


def category_list(request):
    category_list = Category.objects.exclude(name='default')
    context = {
        "category_list": category_list,
    }
    return context


def SearchView(request):
    form = PostSearchForm()
    sQuery = ''
    results = []

    if 'q' in request.GET:
        form = PostSearchForm(request.GET)

        if form.is_valid():
            sQuery = form.cleaned_data['q']
            results = Post.objects.filter(title__icontains = sQuery)

    return render(request, 'blog/search.html', {
        'form' : form,
        'sQuery' : sQuery,
        'posts' : results,
        'navBlog' : True,
    })
