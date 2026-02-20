# blog/middleware.py

from django.http import HttpResponse
from django.utils import timezone
from blog.models import Blog


class BlogCreationLimitMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Only check for logged-in users
        if request.user.is_authenticated:

            # Check if request is blog creation POST
            if request.method == "POST" and request.path == "/add/":

                today = timezone.now().date()

                blog_count = Blog.objects.filter(
                    author=request.user,
                    created_at__date=today
                ).count()

                if blog_count >= 5:
                    return HttpResponse(
                        "Daily blog creation limit reached (5 per day).",
                        status=403
                    )

        response = self.get_response(request)
        return response