from django.shortcuts import render, get_object_or_404
from .models import Post
from django.db.models import F

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
        Post.objects.select_related('category'),
        slug=slug,
        status='published'
    )

    # tambah view
    Post.objects.filter(pk=post.pk).update(
        views=F('views') + 1
    )
    post.refresh_from_db()

    return render(request, 'blog-detail.html', {
        'post': post
    })

def blog(request):
    posts = (
        Post.objects
        .filter(status='published')
        .select_related('category')
        .order_by('-published_at')
    )

    return render(request, 'blog.html', {
        'posts': posts
    })