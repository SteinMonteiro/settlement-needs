from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from .models import RedditPost, IngestionLog


@require_http_methods(["GET"])
def ingestion_status(request):
    """Get status of recent ingestion jobs."""
    logs = IngestionLog.objects.all()[:10]
    stats = {
        'total_posts': RedditPost.objects.count(),
        'valid_posts': RedditPost.objects.filter(is_valid=True).count(),
        'noise_posts': RedditPost.objects.filter(is_noise=True).count(),
        'promotional_posts': RedditPost.objects.filter(is_promotional=True).count(),
        'recent_logs': [
            {
                'task_id': log.task_id,
                'status': log.status,
                'posts_collected': log.posts_collected,
                'posts_filtered': log.posts_filtered,
                'posts_saved': log.posts_saved,
                'started_at': log.started_at.isoformat() if log.started_at else None,
            }
            for log in logs
        ]
    }
    return JsonResponse(stats)


@require_http_methods(["GET"])
def posts_list(request):
    """List all collected posts with filtering options."""
    posts = RedditPost.objects.all()
    
    # Apply filters
    subreddit = request.GET.get('subreddit')
    if subreddit:
        posts = posts.filter(subreddit=subreddit)
    
    is_valid = request.GET.get('is_valid')
    if is_valid is not None:
        posts = posts.filter(is_valid=is_valid.lower() == 'true')
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 20)
    page_obj = paginator.get_page(page)
    
    posts_data = [
        {
            'id': post.id,
            'title': post.title,
            'subreddit': post.subreddit,
            'author': post.author,
            'posted_at': post.posted_at.isoformat(),
            'upvotes': post.upvotes,
            'comments_count': post.comments_count,
            'is_valid': post.is_valid,
            'is_noise': post.is_noise,
            'is_promotional': post.is_promotional,
        }
        for post in page_obj
    ]
    
    return JsonResponse({
        'count': paginator.count,
        'page': page_obj.number,
        'total_pages': paginator.num_pages,
        'results': posts_data,
    })


@require_http_methods(["GET"])
def post_detail(request, pk):
    """Get details of a specific post."""
    post = get_object_or_404(RedditPost, pk=pk)
    return JsonResponse({
        'id': post.id,
        'post_id': post.post_id,
        'title': post.title,
        'content': post.content,
        'subreddit': post.subreddit,
        'author': post.author,
        'url': post.url,
        'posted_at': post.posted_at.isoformat(),
        'upvotes': post.upvotes,
        'comments_count': post.comments_count,
        'is_valid': post.is_valid,
        'is_noise': post.is_noise,
        'noise_reason': post.noise_reason,
        'is_promotional': post.is_promotional,
        'is_duplicate': post.is_duplicate,
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat(),
    })


@require_http_methods(["GET"])
def ingestion_logs(request):
    """List ingestion job logs."""
    logs = IngestionLog.objects.all()
    
    status = request.GET.get('status')
    if status:
        logs = logs.filter(status=status)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(logs, 20)
    page_obj = paginator.get_page(page)
    
    logs_data = [
        {
            'task_id': log.task_id,
            'status': log.status,
            'started_at': log.started_at.isoformat() if log.started_at else None,
            'completed_at': log.completed_at.isoformat() if log.completed_at else None,
            'posts_collected': log.posts_collected,
            'posts_filtered': log.posts_filtered,
            'posts_saved': log.posts_saved,
            'error_message': log.error_message,
        }
        for log in page_obj
    ]
    
    return JsonResponse({
        'count': paginator.count,
        'page': page_obj.number,
        'total_pages': paginator.num_pages,
        'results': logs_data,
    })
