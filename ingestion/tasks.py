import logging
from datetime import datetime, timedelta
import praw
from django.conf import settings
from django.utils import timezone
from celery import shared_task
from .models import RedditPost, IngestionLog
from .filters import NoiseFilter

logger = logging.getLogger('ingestion')


# Target subreddits for data collection
TARGET_SUBREDDITS = [
    'ImmigrationCanada',
    'PersonalFinanceCanada',
    'askTO',
]

# Keywords to filter relevant posts
TARGET_KEYWORDS = [
    'new to canada',
    'copr',
    'settlement',
    'housing',
    'employment',
    'health',
    'language',
    'visa',
    'immigration',
]


def get_reddit_client():
    """Initialize and return Reddit API client."""
    config = settings.REDDIT_CONFIG
    try:
        return praw.Reddit(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            user_agent=config['user_agent'],
            username=config['username'],
            password=config['password'],
        )
    except Exception as e:
        logger.error(f"Failed to initialize Reddit client: {str(e)}")
        raise


def is_relevant_post(post):
    """
    Check if a post is relevant based on keywords.
    """
    text = f"{post.title} {post.selftext}".lower()
    return any(keyword in text for keyword in TARGET_KEYWORDS)


def collect_posts_from_subreddit(reddit, subreddit_name, limit=100):
    """
    Collect posts from a specific subreddit.
    
    Args:
        reddit: PRAW Reddit instance
        subreddit_name: Name of subreddit (without r/)
        limit: Number of posts to collect
    
    Returns:
        List of raw post data dictionaries
    """
    posts = []
    try:
        subreddit = reddit.subreddit(subreddit_name)
        logger.info(f"Fetching posts from r/{subreddit_name}")
        
        for submission in subreddit.new(limit=limit):
            if is_relevant_post(submission):
                post_data = {
                    'post_id': submission.id,
                    'subreddit': subreddit_name,
                    'author': submission.author.name if submission.author else '[deleted]',
                    'title': submission.title,
                    'content': submission.selftext,
                    'url': submission.url,
                    'upvotes': submission.score,
                    'comments_count': submission.num_comments,
                    'posted_at': timezone.make_aware(
                        datetime.fromtimestamp(submission.created_utc)
                    ),
                }
                posts.append(post_data)
        
        logger.info(f"Collected {len(posts)} relevant posts from r/{subreddit_name}")
        return posts
    
    except Exception as e:
        logger.error(f"Error collecting posts from r/{subreddit_name}: {str(e)}")
        return []


@shared_task(bind=True)
def ingest_reddit_posts(self):
    """
    Main Celery task to ingest Reddit posts.
    Collects, filters, and stores posts in database.
    """
    log_entry = IngestionLog.objects.create(
        task_id=self.request.id,
        status='running',
        started_at=timezone.now()
    )
    
    try:
        reddit = get_reddit_client()
        noise_filter = NoiseFilter()
        all_posts = []
        
        # Collect posts from all target subreddits
        for subreddit_name in TARGET_SUBREDDITS:
            posts = collect_posts_from_subreddit(reddit, subreddit_name, limit=100)
            all_posts.extend(posts)
        
        log_entry.posts_collected = len(all_posts)
        logger.info(f"Total posts collected: {len(all_posts)}")
        
        # Filter posts
        filtered_posts = []
        for post_data in all_posts:
            is_valid, reasons = noise_filter.filter_post(post_data)
            
            if is_valid:
                filtered_posts.append(post_data)
            else:
                log_entry.posts_filtered += 1
                logger.debug(f"Filtered post {post_data['post_id']}: {reasons}")
        
        logger.info(f"Posts after filtering: {len(filtered_posts)}")
        
        # Save to database
        saved_count = 0
        for post_data in filtered_posts:
            try:
                reddit_post, created = RedditPost.objects.update_or_create(
                    post_id=post_data['post_id'],
                    defaults={
                        'subreddit': post_data['subreddit'],
                        'author': post_data['author'],
                        'title': post_data['title'],
                        'content': post_data['content'],
                        'url': post_data['url'],
                        'upvotes': post_data['upvotes'],
                        'comments_count': post_data['comments_count'],
                        'posted_at': post_data['posted_at'],
                        'is_valid': True,
                    }
                )
                if created:
                    saved_count += 1
            except Exception as e:
                logger.error(f"Error saving post {post_data['post_id']}: {str(e)}")
        
        log_entry.posts_saved = saved_count
        log_entry.status = 'completed'
        log_entry.completed_at = timezone.now()
        log_entry.save()
        
        logger.info(
            f"Ingestion completed. Collected: {log_entry.posts_collected}, "
            f"Filtered: {log_entry.posts_filtered}, Saved: {log_entry.posts_saved}"
        )
        
        return {
            'status': 'success',
            'posts_collected': log_entry.posts_collected,
            'posts_filtered': log_entry.posts_filtered,
            'posts_saved': log_entry.posts_saved,
        }
    
    except Exception as e:
        log_entry.status = 'failed'
        log_entry.error_message = str(e)
        log_entry.completed_at = timezone.now()
        log_entry.save()
        
        logger.error(f"Ingestion task failed: {str(e)}", exc_info=True)
        raise
