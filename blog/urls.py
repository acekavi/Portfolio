from django.urls import path
from . import views

from django.utils.translation import gettext_lazy as _

app_name = "blog"

urlpatterns = [
    path('', views.blogList.as_view(), name="blog-list"),
    path('search/', views.SearchView, name='search-list'),
    path('<slug:slug>/', views.BlogDetail.as_view(), name="blog-detail"),
    path(_('filter/<slug:slug>/'), views.CategoryListView.as_view(), name='category-list'),

    path('favorite/<int:id>/', views.favorites, name='favorites'),
    path('like/<int:id>/', views.likes, name='likes'),

]
