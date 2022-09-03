from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status')
    prepopulated_fields = {
        "slug": ("title",),
    }


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'status')
    list_filter = ('status', 'publish')
    search_fields = ('name', 'email', 'content')
