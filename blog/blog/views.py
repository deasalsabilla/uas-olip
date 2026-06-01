from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from django.db.models import F
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth


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

def statistik(request):

    total_post = Post.objects.count()
    total_category = Category.objects.count()
    total_views = Post.objects.aggregate(
        total=Sum('views')
    )['total'] or 0

    total_published = Post.objects.filter(
        status='published'
    ).count()

    # Artikel per kategori
    category_stats = (
        Category.objects
        .annotate(total=Count('posts'))
        .order_by('-total')
    )

    category_labels = [
        item.name for item in category_stats
    ]

    category_data = [
        item.total for item in category_stats
    ]

    # Artikel per bulan
    monthly_stats = (
        Post.objects
        .filter(status='published')
        .annotate(month=TruncMonth('published_at'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )

    monthly_labels = [
        item['month'].strftime('%b %Y')
        for item in monthly_stats
        if item['month']
    ]

    monthly_data = [
        item['total']
        for item in monthly_stats
    ]

    top_posts = (
        Post.objects
        .filter(status='published')
        .order_by('-views')[:5]
    )

    context = {
        'total_post': total_post,
        'total_category': total_category,
        'total_views': total_views,
        'total_published': total_published,

        'category_labels': category_labels,
        'category_data': category_data,

        'monthly_labels': monthly_labels,
        'monthly_data': monthly_data,

        'top_posts': top_posts,
    }

    return render(request, 'statistik.html', context)