from django.shortcuts import render
from blog.models import Post


def about_me(request):
    return render(
        request,
        'single_pages/about_me.html'
    )


def landing(request):
    recent_posts = Post.objects.order_by('-pk')[:3]
    return render(
        request,
        'single_pages/landing.html',
        {
            'recent_posts': recent_posts,
        }
    )

def page_not_found(request, exception):
    """
    404 Page not found
    """
    return render(
        request,
        'common/404.html',
    )
