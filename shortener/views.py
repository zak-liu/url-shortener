from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ShortenedURL, ClickDetail
from .utils import generate_short_code

def create_url(request):
    """
    Handle short URL creation. Includes a fix to strip whitespace from input URLs
    to prevent malformed redirection errors.
    """
    short_url = None
    
    if request.method == "POST":
        # .strip() is crucial to remove accidental spaces that cause 404/malformed path errors
        original_url = request.POST.get("original_url", "").strip()
        
        if request.user.is_authenticated:
            # Generate a new unique code for the link
            short_code = generate_short_code()
            
            # Save the mapping between the long URL and short code to the database
            url_instance = ShortenedURL.objects.create(
                original_url=original_url,
                short_code=short_code,
                user=request.user
            )
            
            # Build the absolute URL. Note: Ensure your urls.py pattern matches this format.
            # Usually, shorteners do not use a trailing slash for cleaner links.
            short_url = request.build_absolute_uri(f'/{short_code}')
        else:
            return render(request, "shortener/index.html", {"error": "Please login first."})
            
    return render(request, "shortener/index.html", {"short_url": short_url})


def redirect_url(request, short_code):
    """
    Redirect users to the original destination and log visitor metadata (IP and User Agent).
    """
    # Retrieve the record or return a 404 if the code doesn't exist
    url_record = get_object_or_404(ShortenedURL, short_code=short_code)
    
    # Capture the real visitor IP when deployed on Render (via X-Forwarded-For header)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    
    if x_forwarded_for:
        # Extract the first IP from the comma-separated list provided by the proxy
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        # Fallback to remote address for local development environments
        ip = request.META.get('REMOTE_ADDR')
        
    # Create a click log entry for analytics
    ClickDetail.objects.create(
        url_record=url_record,
        ip_address=ip,
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    # Perform the redirection to the original destination
    return redirect(url_record.original_url)


@login_required
def url_stats(request):
    """
    Display a list of URLs created by the current user along with their click history.
    """
    # Fetch user-owned URLs from newest to oldest
    user_urls = ShortenedURL.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'shortener/stats.html', {'urls': user_urls})