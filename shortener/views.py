# django imports for views and authentication
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View  
from django.contrib.auth.mixins import LoginRequiredMixin 

# Import models
from .models import ShortenedURL, ClickDetail

# REST Framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema, OpenApiExample

# Import Serializer
from .serializers import ShortenedURLSerializer

# --- REST API Endpoints (For Mobile/Third-party/Swagger) ---

class ShortLinkCreateAPI(APIView):
    """
    API endpoint to create a shortened URL. 
    Uses Serializer to handle short_code generation logic centrally.
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
            # Logic encapsulated in Serializer.create()
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShortLinkListAPI(APIView):
    """
    API endpoint to list all short links created by the current user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Uses centralized manager method 'for_user'
        links = ShortenedURL.objects.for_user(request.user)
        serializer = ShortenedURLSerializer(links, many=True)
        return Response(serializer.data)


# --- Web Interface Views (Browser Based) ---

class CreateURLView(LoginRequiredMixin, View):
    """
    Web view for the homepage. Reuses Serializer to keep code DRY.
    """
    def get(self, request):
        return render(request, "shortener/index.html")

    def post(self, request):
        # Reuse Serializer for web form to ensure consistent logic
        data = {"original_url": request.POST.get("original_url", "").strip()}
        serializer = ShortenedURLSerializer(data=data)
        
        if serializer.is_valid():
            # Consistent with API behavior
            instance = serializer.save(user=request.user)
            short_url = request.build_absolute_uri(f'/{instance.short_code}')
            return render(request, "shortener/index.html", {"short_url": short_url})
        
        return render(request, "shortener/index.html", {"error": "Invalid URL provided."})


class URLRedirectView(LoginRequiredMixin, View):
    """
    Handles redirection and visitor tracking. 
    Captures real IP address even behind proxies (e.g. Render).
    """
    def get(self, request, short_code):
        url_record = get_object_or_404(ShortenedURL, short_code=short_code)
        
        # Capture IP considering proxy headers
        x_fwd = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_fwd.split(',')[0].strip() if x_fwd else request.META.get('REMOTE_ADDR')
            
        # Log analytics
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
        # Uses the same manager method as API for consistency
        user_urls = ShortenedURL.objects.for_user(request.user)
        return render(request, 'shortener/stats.html', {'urls': user_urls})