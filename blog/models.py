from statistics import mode
from django.utils import timezone
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model

## Category model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

## Series model
class Series(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name

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
    overview = models.TextField(max_length=500, default="")
    blog_series = models.ForeignKey(Series, on_delete=models.PROTECT, default=1)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey (User, on_delete=models.CASCADE, related_name='blog_posts')
    content = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=options, default='draft')
    favorites = models.ManyToManyField(User, related_name='favorite', default=None, blank=True)
    likes = models.ManyToManyField(User, related_name="Likes", default=None, blank=True)

    objects = models.Manager()
    postManager = PostManager()

    def get_absolute_url(self):
        return reverse('blog:blog-detail', args=[self.slug])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(get_user_model() , on_delete=models.CASCADE)
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self' , null=True , blank=True , on_delete=models.CASCADE , related_name='replies')
    status = models.BooleanField(default=True)

    class Meta:
        ordering=['-publish']

    def __str__(self):
        return str(self.author) + ' comment ' + str(self.content)

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
    
