"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from . import settings
from django.utils.translation import gettext_lazy as _

urlpatterns = [
	path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
  path('tubelight/', admin.site.urls),
	path(_('ckeditor/'), include('ckeditor_uploader.urls')),

	path("user/", include('accounts.urls', namespace="accounts")),
	path('user/', include('django.contrib.auth.urls')),
	path('', include('base.urls')),
	path('blog/', include('blog.urls', namespace='blog')),
]

handler404 = 'admin_honeypot.views.handler404'

# if settings.dev.DEBUG:
# 	urlpatterns += [
# 		path(_('media/<path>'), serve, {
# 			'document_root': settings.dev.MEDIA_ROOT
# 		}),
# 	]