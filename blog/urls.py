from unicodedata import name
from django.urls import path, include
from . import views

app_name = "blog"

urlpatterns = [
    path('', views.blogList, name="blog-list"),
    path('search/', views.SearchView, name='search-list'),
    path('<slug:slug>/', views.BlogDetail.as_view(), name="blog-detail"),
    path('filter/<category>/', views.CategoryListView.as_view(), name='category-list'),

]
