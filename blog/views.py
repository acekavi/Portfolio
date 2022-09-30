from django.shortcuts import get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView,ListView
from .forms import NewCommentForm
from .models import Category, Post, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

# Create your views here.
class blogList(ListView):
    template_name = 'blog/list.html'
    model= Post
    context_object_name ='posts'
    paginate_by = 6
    queryset = Post.postManager.all()
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['navBlog'] = True
        data["pageTitle"] = 'All Posts'
        data["heading"] = "Join the journey"
        data["secondary"] = "Wisdom means to choose now what will make sense later"
        data["author"] = "Tracee Ellis Ross"
        return data


class CategoryListView(ListView):
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    model= Post
    paginate_by = 6

    def get_queryset(self):
       return Post.postManager.filter(category__name=self.request.resolver_match.kwargs['slug'])

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['navBlog'] = True
        data["pageTitle"] = self.request.resolver_match.kwargs['slug']
        data["heading"] = f"All about {self.request.resolver_match.kwargs['slug']}"
        data["secondary"] = "Live every day like it is your last and learn everyday like you will live forever"
        data["author"] = "Mahatma Gandhi"
        return data


class SearchListView(ListView):
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    model= Post
    # paginate_by = 6
    
    def get_queryset(self):
        sQuery = self.request.GET['q']
        # results = Post.objects.filter(title__search = sQuery)
        results = Post.objects.annotate(search=SearchVector('title', 'content'),).filter(search=SearchQuery(sQuery))

        # vector = SearchVector('title', weight='A') + SearchVector('overview', weight='B')
        # query= SearchQuery(sQuery)
        # results = Post.objects.annotate(rank=SearchRank(vector,query,cover_density=True)).order_by('-rank')
        return results

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        heading = f"All the posts containing '{self.request.GET['q'].capitalize()}'"
        if not data['posts']:
            heading = "No Results found!"

        data['navBlog'] = True
        data["pageTitle"] = "Search"
        data["heading"] = heading
        data["secondary"] = "Quit everything until you find something that you just cannot quit"
        data["author"] = "Bobcat Goldthwait"
        return data


class BlogDetail(DetailView):
    template_name= 'blog/details.html'
    model= Post
    context_object_name= 'post'

    def get_context_data(self, **kwargs):
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
                    parent = None

            new_comment = Comment(content=content , author = self.request.user , post=self.get_object() , parent=parent)
            new_comment.save()
            return redirect(self.request.path_info)

# context processor
def category_list(request):
    category_list = Category.objects.exclude(name='default')
    context = {
        "category_list": category_list,
    }
    return context


@login_required
def favorites(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user in post.favorites.all():
        post.favorites.remove(request.user)
    else:
        post.favorites.add(request.user)
    return HttpResponseRedirect(reverse('blog:blog-detail', kwargs={ 'slug': post.slug }))

@login_required
def likes(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('blog:blog-detail', kwargs={ 'slug': post.slug }))
