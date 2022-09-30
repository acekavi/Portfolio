from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
## Category model
class ArtStyle(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Artwork model
class Artwork(models.Model):
  title = models.CharField(max_length=250)
  slug = models.SlugField(max_length=250, unique_for_date='publish')
  description = models.TextField(max_length=500, default="")
  thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
  artFile = models.ImageField(upload_to='artworks/', default="artworks/default.jpg")
  prompt = models.TextField(max_length=500, default="", blank=True)
  style = models.ForeignKey(ArtStyle, on_delete=models.PROTECT, default=1)
  publish = models.DateTimeField(default=timezone.now)
  author = models.ForeignKey (User, on_delete=models.CASCADE, related_name='art_designer')
  likes = models.ManyToManyField(User, related_name="art_likes", default=None, blank=True)
  behance = models.URLField(max_length=250, blank=True, null=True)

  def get_absolute_url(self):
        return reverse('base:designs-details', args=[self.slug])

  def __str__(self):
      return self.title

## Comment Model
class ArtComment(models.Model):
  artwork = models.ForeignKey(Artwork , on_delete=models.CASCADE, related_name="art_comments")
  author = models.ForeignKey(get_user_model() , on_delete=models.CASCADE)
  content = models.TextField()
  publish = models.DateTimeField(auto_now_add=True)
  parent = models.ForeignKey('self' , null=True , blank=True , on_delete=models.CASCADE , related_name='art_replies')
  status = models.BooleanField(default=True)

  class Meta:
      ordering=['-publish']

  def __str__(self):
      return str(self.author) + ' comment ' + str(self.content)

  @property
  def children(self):
      return ArtComment.objects.filter(parent=self).reverse()

  @property
  def is_parent(self):
      if self.parent is None:
          return True
      return False


##  Project model
class Project(models.Model):

    class ProjectManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    overview = models.TextField(max_length=500, default="")
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey (User, on_delete=models.CASCADE, related_name='project_dev')
    status = models.CharField(max_length=10, choices=options, default='draft')
    github = models.URLField(max_length=250, blank=True, null=True)
    demo = models.URLField(max_length=250, blank=True, null=True)

    objects = models.Manager()
    projectManager = ProjectManager()

    def get_absolute_url(self):
        return reverse('base:project-details', args=[self.slug])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
