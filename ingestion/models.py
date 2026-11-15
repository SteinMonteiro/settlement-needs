from django.db import models
from django.utils import timezone


class RedditPost(models.Model):
    """
    Model to store raw Reddit posts collected from targeted subreddits.
    """
    # Reddit metadata
    post_id = models.CharField(max_length=100, unique=True, db_index=True)
    subreddit = models.CharField(max_length=100, db_index=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=500)
    content = models.TextField()
    url = models.URLField(unique=True)
    
    # Engagement metrics
    upvotes = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    
    # Timestamps
    posted_at = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Classification and filtering
    is_duplicate = models.BooleanField(default=False, db_index=True)
    is_promotional = models.BooleanField(default=False, db_index=True)
    is_noise = models.BooleanField(default=False, db_index=True)
    noise_reason = models.CharField(
        max_length=255, 
        null=True, 
        blank=True,
        help_text="Reason why post was marked as noise"
    )
    is_valid = models.BooleanField(default=True, db_index=True)
    
    class Meta:
        ordering = ['-posted_at']
        indexes = [
            models.Index(fields=['subreddit', 'posted_at']),
            models.Index(fields=['is_valid', 'is_noise', 'posted_at']),
        ]
    
    def __str__(self):
        return f"{self.subreddit}: {self.title[:50]}"


class IngestionLog(models.Model):
    """
    Track ingestion jobs for debugging and monitoring.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    task_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    posts_collected = models.IntegerField(default=0)
    posts_filtered = models.IntegerField(default=0)
    posts_saved = models.IntegerField(default=0)
    error_message = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"Ingestion {self.task_id}: {self.status}"
