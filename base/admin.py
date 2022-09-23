from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Artwork)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'style')
    prepopulated_fields = {
        "slug": ("title",),
    }

@admin.register(models.Project)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status')
    prepopulated_fields = {
        "slug": ("title",),
    }

@admin.register(models.ArtComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'status')
    list_filter = ('status', 'publish')

admin.site.register(models.ArtStyle)