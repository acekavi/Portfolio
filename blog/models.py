from importlib.resources import contents
from pyexpat import model
from unicodedata import name
from django.utils import timezone
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.urls import reverse


##  Post model
class Post(models.Model):

    class PostManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey (User, on_delete=models.CASCADE, related_name='blog_posts')
    content = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=options, default='draft')

    objects = models.Manager()
    postManager = PostManager()

    def get_absolute_url(self):
        return reverse('blog:blog-detail', args=[self.slug])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


## Comment model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=50)
    email = models.EmailField()
    content = RichTextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
            ordering = ('publish',)

    def __str__(self):
        return f"Comment by {self.name}"