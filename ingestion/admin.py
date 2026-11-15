from django.contrib import admin
from .models import RedditPost, IngestionLog


@admin.register(RedditPost)
class RedditPostAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'subreddit',
        'author',
        'posted_at',
        'is_valid',
        'is_noise',
        'is_promotional',
        'upvotes',
        'comments_count',
    ]
    list_filter = [
        'subreddit',
        'is_valid',
        'is_noise',
        'is_promotional',
        'is_duplicate',
        'posted_at',
    ]
    search_fields = ['title', 'content', 'author', 'subreddit']
    readonly_fields = ['post_id', 'created_at', 'updated_at', 'url']
    fieldsets = (
        ('Reddit Data', {
            'fields': ('post_id', 'subreddit', 'author', 'title', 'content', 'url')
        }),
        ('Engagement', {
            'fields': ('upvotes', 'comments_count')
        }),
        ('Filtering & Classification', {
            'fields': ('is_valid', 'is_noise', 'noise_reason', 'is_promotional', 'is_duplicate')
        }),
        ('Timestamps', {
            'fields': ('posted_at', 'created_at', 'updated_at')
        }),
    )


@admin.register(IngestionLog)
class IngestionLogAdmin(admin.ModelAdmin):
    list_display = [
        'task_id',
        'status',
        'started_at',
        'posts_collected',
        'posts_filtered',
        'posts_saved',
    ]
    list_filter = ['status', 'started_at']
    readonly_fields = ['task_id', 'started_at', 'completed_at']
    fieldsets = (
        ('Task Information', {
            'fields': ('task_id', 'status')
        }),
        ('Timeline', {
            'fields': ('started_at', 'completed_at')
        }),
        ('Statistics', {
            'fields': ('posts_collected', 'posts_filtered', 'posts_saved')
        }),
        ('Errors', {
            'fields': ('error_message',)
        }),
    )
