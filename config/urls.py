"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Authentication routes (django-allauth)
    path('', include('shortener.urls')),        # Main app routes (including API endpoints and documentation)
    path('accounts/', include('allauth.urls')), # Authentication routes (login, logout, social auth)

    # API Documentation (Staff Only)
    path('api/schema/', login_required(SpectacularAPIView.as_view()), name='schema'),
    path('api/docs/', login_required(SpectacularSwaggerView.as_view(url_name='schema')), name='swagger-ui'),
]

# Admin route only in DEBUG mode for security hardening in production
if settings.DEBUG:
    urlpatterns = [
        path('admin/', admin.site.urls),
    ] + urlpatterns