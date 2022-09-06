from unicodedata import name
from django.urls import path, include
from . import views

app_name = "blog"

urlpatterns = [
    path('', views.blogList, name="blog-list"),
    path('<slug:post>/', views.blogDetail, name="blog-detail"),
    path('filter/<category>/', views.CategoryListView.as_view(), name='filter-list')
]
