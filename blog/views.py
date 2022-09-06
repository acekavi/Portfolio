from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewCommentForm
from .models import Category, Post

from django.views.generic import ListView

# Create your views here.
def blogList(request):

    all_posts = Post.postManager.all()

    return render(request, 'blog/index.html', {
        'posts' : all_posts,
        'blog_page' : 'active',
    })


def blogDetail(request, post):

    post = get_object_or_404(Post, slug = post, status = "published")
    comments = post.comments.filter(status = True)

    user_comment = None

    if request.method == 'POST':
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.post = post
            user_comment.save()
            return redirect('.')
    else:
        comment_form = NewCommentForm()

    return render(request, 'blog/details.html', {
        'post' : post,
        'comments' : user_comment,
        'comments' : comments,
        'comment_form' : comment_form,
        'blog_page' : 'active',
    })

class CategoryListView(ListView):
    template_name = 'blog/category.html'
    context_object_name = 'catList'

    def get_queryset(self):
        content = {
            'cat': self.kwargs['category'],
            'posts': Post.objects.filter(category__name=self.kwargs['category']).filter(status='published'),
            'blog_page' : 'active',
        }
        return content


def category_list(request):
    category_list = Category.objects.exclude(name='default')
    context = {
        "category_list": category_list,
    }
    return context        