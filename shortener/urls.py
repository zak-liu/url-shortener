# django imports for URL routing
from django.urls import path

# Import views and API classes
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views

urlpatterns = [
    # Browser Routes (Web CBVs)
    path('', views.CreateURLView.as_view(), name='create_url'),
    path('stats/', views.URLStatsView.as_view(), name='url_stats'),
    path('<str:short_code>', views.URLRedirectView.as_view(), name='redirect'),
    
    # REST API Routes (DRF APIViews)
    path('api/create/', views.ShortLinkCreateAPI.as_view(), name='api_create'),
    path('api/list/', views.ShortLinkListAPI.as_view(), name='api_list'),

    # Documentation UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]