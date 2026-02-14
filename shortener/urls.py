# django imports for URL routing
from django.urls import path, include
from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required

# Import views and API classes
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views

urlpatterns = [
    # Core Django and Authentication Routes
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    
    # Browser Routes (Web CBVs)
    path('', views.CreateURLView.as_view(), name='create_url'),
    path('stats/', views.URLStatsView.as_view(), name='url_stats'),
    path('<str:short_code>', views.URLRedirectView.as_view(), name='redirect'),
    
    # REST API Routes (DRF APIViews)
    path('api/create/', views.ShortLinkCreateAPI.as_view(), name='api_create'),
    path('api/list/', views.ShortLinkListAPI.as_view(), name='api_list'),

    # Documentation UI
    path('api/schema/', login_required(SpectacularAPIView.as_view()), name='schema'),
    path('api/docs/', login_required(SpectacularSwaggerView.as_view(url_name='schema')), name='swagger-ui'),
]