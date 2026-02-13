from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_url, name='create_url'),
    path('stats/', views.url_stats, name='url_stats'), # Analytics dashboard
    path('<str:short_code>/', views.redirect_url, name='redirect'),
]