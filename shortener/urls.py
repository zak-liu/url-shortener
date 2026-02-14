# django imports for URL routing
from django.urls import path

# Import views and API classes
from . import views

urlpatterns = [
    # Browser Routes (Web CBVs)
    path('', views.CreateURLView.as_view(), name='create_url'),
    path('stats/', views.URLStatsView.as_view(), name='url_stats'),
    path('<str:short_code>', views.URLRedirectView.as_view(), name='redirect'),
    
    # REST API Routes (DRF APIViews)
    path('api/create/', views.ShortLinkCreateAPI.as_view(), name='api_create'),
    path('api/list/', views.ShortLinkListAPI.as_view(), name='api_list'),
]
