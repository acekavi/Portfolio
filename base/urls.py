from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _

app_name = "base"

urlpatterns = [
    path('', views.indexView, name="homepage"),
    path('projects/', views.ProjectsView.as_view(), name="projects"),
    path('projects/<slug:slug>/', views.ProjectDetails.as_view(), name="project-details"),
    path('designs/', views.DesignsView.as_view(), name="designs"),
    path('designs/<slug:slug>/', views.DesignDetails.as_view(), name="designs-details"),
    # path('search/', views.SearchListView.as_view(), name='search-list'),
    # path('<slug:slug>/', views.BlogDetail.as_view(), name="blog-detail"),
    # path(_('filter/<slug:slug>/'), views.CategoryListView.as_view(), name='category-list'),

    # path('favorite/<int:id>/', views.favorites, name='favorites'),
    # path('like/<int:id>/', views.likes, name='likes'),

]
