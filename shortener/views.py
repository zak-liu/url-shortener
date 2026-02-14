# django imports for views and authentication
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View  # Base class for Web Views
from django.contrib.auth.mixins import LoginRequiredMixin # Mixin for class-based auth

# Import models and utilities
from .models import ShortenedURL, ClickDetail
from .utils import generate_short_code

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample

from .serializers import ShortenedURLSerializer

# --- API Endpoints (For Mobile/Third-party Integration) ---
class ShortLinkCreateAPI(APIView):
    """
    API endpoint to create a shortened URL. 
    Enforces authentication to ensure link ownership.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ShortenedURLSerializer

    @extend_schema(
        request=ShortenedURLSerializer,
        responses={201: ShortenedURLSerializer},
        examples=[
            OpenApiExample(
                'Valid API Request',
                value={"original_url": "https://www.google.com"},
                request_only=True,
            )
        ]
    )
    def post(self, request):
        serializer = ShortenedURLSerializer(data=request.data)
        if serializer.is_valid():
            short_code = generate_short_code()
            # Explicitly associate the link with the logged-in user
            serializer.save(user=request.user, short_code=short_code)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShortLinkListAPI(APIView):
    """
    API endpoint to list all short links created by the current user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        links = ShortenedURL.objects.filter(user=request.user).order_by('-created_at')
        serializer = ShortenedURLSerializer(links, many=True)
        return Response(serializer.data)


# --- Web Interface Views (For Browser Access) ---
class CreateURLView(LoginRequiredMixin, View):
    """
    Web view for the homepage to create short links via a browser form.
    """
    def get(self, request):
        return render(request, "shortener/index.html")

    def post(self, request):
        original_url = request.POST.get("original_url", "").strip()
        short_code = generate_short_code()
        
        ShortenedURL.objects.create(
            original_url=original_url,
            short_code=short_code,
            user=request.user
        )
        
        short_url = request.build_absolute_uri(f'/{short_code}')
        return render(request, "shortener/index.html", {"short_url": short_url})


class URLRedirectView(LoginRequiredMixin, View):
    """
    Handles redirection and visitor tracking. 
    Requires login to prevent unauthorized use of the link.
    """
    def get(self, request, short_code):
        url_record = get_object_or_404(ShortenedURL, short_code=short_code)
        
        # Capture visitor IP through proxy for Render deployment
        x_fwd = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_fwd.split(',')[0].strip() if x_fwd else request.META.get('REMOTE_ADDR')
            
        # Log analytics metadata
        ClickDetail.objects.create(
            url_record=url_record,
            ip_address=ip,
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        return redirect(url_record.original_url)


class URLStatsView(LoginRequiredMixin, View):
    """
    Displays the analytics dashboard for the logged-in user.
    """
    def get(self, request):
        user_urls = ShortenedURL.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'shortener/stats.html', {'urls': user_urls})