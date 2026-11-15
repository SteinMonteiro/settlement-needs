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
# Based on "Searching for settlement information on Reddit" (Monteiro, 2024)
# Ordered by frequency of settlement-related posts
TARGET_SUBREDDITS = [
    'ImmigrationCanada',      # 24.6% of posts in paper
    'PersonalFinanceCanada',  # 17.5% of posts in paper
    'askTO',                  # 4.1% of posts in paper
    'legaladvicecanada',      # 2.1% of posts in paper
]

# Keywords to filter relevant posts
# Derived from keywords analysis in Monteiro 2024 paper
# These keywords identify newcomers seeking settlement information and resources
TARGET_KEYWORDS = [
    'new to canada',
    'just arrived in canada',
    'just migrated in canada',
    'just immigrated in canada',
    'newcomer to canada',
    'newcomers to canada',
    'newcomer in canada',
    'new immigrant in canada',
    'new migrant in canada',
    'received my copr',
    'received our copr',
    'confirmation of permanent residency',
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
    Check if a post is relevant based on TARGET_KEYWORDS.
    
    Implements keyword filtering methodology from Monteiro 2024 paper.
    Posts are considered relevant if they contain any of the target keywords
    in the title or content (case-insensitive comparison).
    
    This identifies posts from newcomers seeking settlement resources and advice.
    """
    text = f"{post.title} {post.selftext}".lower()
    return any(keyword in text for keyword in TARGET_KEYWORDS)


def collect_posts_from_subreddit(reddit, subreddit_name, limit=500):
    """
    Collect posts from a specific subreddit.
    
    Methodology based on "Searching for settlement information on Reddit" (Monteiro, 2024).
    Fetches recent posts from the subreddit and filters by TARGET_KEYWORDS to identify
    posts from newcomers seeking settlement resources and information.
    
    Args:
        reddit: PRAW Reddit instance
        subreddit_name: Name of subreddit (without r/)
        limit: Number of posts to collect (default: 500 to capture ~1 week of activity)
    
    Returns:
        List of raw post data dictionaries with fields:
        - post_id, subreddit, author, title, content, url
        - upvotes, comments_count, posted_at
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
    Main Celery task to ingest Reddit posts from settlement-related subreddits.
    
    Runs weekly (configurable via DATA_INGESTION_INTERVAL in settings.py).
    
    Data collection methodology based on "Searching for settlement information on Reddit" 
    (Monteiro, 2024). Process:
    1. Connects to Reddit API (PRAW)
    2. Fetches ~500 recent posts from each target subreddit
    3. Filters by TARGET_KEYWORDS to identify settlement-related posts
    4. Applies NoiseFilter to remove spam, promotional content, and low-quality posts
    5. Stores valid posts in database
    6. Logs results for monitoring
    
    Returns:
        dict: Summary of ingestion results (posts_collected, posts_filtered, posts_saved)
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
