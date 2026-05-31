from django.shortcuts import render, get_object_or_404
from .models import Post

def home(request):
    latest_posts = Post.objects.filter(
        status='published'
    ).select_related('category').order_by('-published_at')[:6]

    context = {
        'latest_posts': latest_posts
    }

    return render(request, 'index.html', context)

def post_detail(request, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        status='published'
    )

    return render(request, 'blog-detail.html', {
        'post': post
    })