from django.contrib import admin
from .models import Category, Post


# =========================================
# CATEGORY ADMIN
# =========================================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'slug',
        'created_at',
    )

    search_fields = (
        'name',
    )

    prepopulated_fields = {
        'slug': ('name',)
    }

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    list_per_page = 10


# =========================================
# POST ADMIN
# =========================================
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'category',
        'status',
        'views',
        'created_at',
    )

    list_filter = (
        'status',
        'category',
        'created_at',
    )

    search_fields = (
        'title',
        'excerpt',
        'content',
    )

    prepopulated_fields = {
        'slug': ('title',)
    }

    readonly_fields = (
        'views',
        'created_at',
        'updated_at',
    )

    list_editable = (
        'status',
    )

    date_hierarchy = 'created_at'

    list_per_page = 10

    fieldsets = (

        ('Post Information', {
            'fields': (
                'title',
                'slug',
                'category',
                'status',
            )
        }),

        ('Content', {
            'fields': (
                'thumbnail',
                'excerpt',
                'content',
            )
        }),

        ('Statistics', {
            'fields': (
                'views',
            )
        }),

        ('Publication', {
            'fields': (
                'published_at',
            )
        }),

        ('System Information', {
            'classes': (
                'collapse',
            ),
            'fields': (
                'created_at',
                'updated_at',
            )
        }),

    )