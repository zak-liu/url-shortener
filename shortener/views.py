from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ShortenedURL, ClickDetail
from .utils import generate_short_code

def create_url(request):
    """
    Handle URL creation and display the result on the same page.
    """
    short_url = None
    
    if request.method == "POST":
        original_url = request.POST.get("original_url")
        
        if request.user.is_authenticated:
            # Generate a unique short code
            short_code = generate_short_code()
            
            # Save to database
            url_instance = ShortenedURL.objects.create(
                original_url=original_url,
                short_code=short_code,
                user=request.user
            )
            
            # Build the full absolute URL (e.g., http://127.0.0.1:8000/5JMCFc)
            # This makes the link clickable for the user
            short_url = request.build_absolute_uri(f'/{short_code}')
        else:
            # Return an error message if the user is not logged in
            return render(request, "shortener/index.html", {"error": "Please login first."})
            
    # Return the index page with the newly created short_url (if any)
    return render(request, "shortener/index.html", {"short_url": short_url})


def redirect_url(request, short_code):
    """
    View to redirect to the original URL and log the visitor's IP address.
    """
    # 1. Fetch the URL record from the database
    url_record = get_object_or_404(ShortenedURL, short_code=short_code)
    
    # 2. Capture the visitor's IP address
    # This checks 'HTTP_X_FORWARDED_FOR' first, which is required for environments like Render.
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    
    if x_forwarded_for:
        # The header may contain a list of IPs (e.g., "client_ip, proxy_ip").
        # We take the first one and use .strip() to remove any whitespace.
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        # Fallback to REMOTE_ADDR for direct connections (e.g., localhost).
        ip = request.META.get('REMOTE_ADDR')
        
    # 3. Log the click information into the ClickDetail model
    ClickDetail.objects.create(
        url_record=url_record,
        ip_address=ip,
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    # 4. Redirect the user to the original long URL
    return redirect(url_record.original_url)


@login_required
def url_stats(request):
    """
    Retrieve all shortened URLs created by the current authenticated user
    along with their detailed click statistics.
    """
    # Fetch URLs owned by the user, ordered by creation time (newest first)
    user_urls = ShortenedURL.objects.filter(user=request.user).order_by('-created_at')
    
    # Render the stats page
    return render(request, 'shortener/stats.html', {'urls': user_urls})