import re
import logging
from difflib import SequenceMatcher

logger = logging.getLogger('ingestion')


class NoiseFilter:
    """
    Filter out irrelevant, duplicate, and promotional posts.
    """
    
    # Common promotional patterns
    PROMOTIONAL_PATTERNS = [
        r'(visit|check out|click here|sign up|join us|contact us)',
        r'(www\.|https?://)',
        r'(ad|advertisement|sponsored)',
        r'(dm|dm me|message me|contact me)',
    ]
    
    # Common spam/bot indicators
    SPAM_PATTERNS = [
        r'crypto|bitcoin|nft|forex|gambling',
        r'buy now|limited time|act fast|hurry',
        r'make money fast|easy cash|work from home',
    ]
    
    # Minimum content quality thresholds
    MIN_TITLE_LENGTH = 10
    MIN_CONTENT_LENGTH = 20
    
    def __init__(self):
        self.compiled_promotional = [re.compile(pattern, re.IGNORECASE) for pattern in self.PROMOTIONAL_PATTERNS]
        self.compiled_spam = [re.compile(pattern, re.IGNORECASE) for pattern in self.SPAM_PATTERNS]
    
    def filter_post(self, post_data):
        """
        Filter a post and return (is_valid, reasons_list).
        """
        reasons = []
        
        # Check basic content quality
        if len(post_data['title']) < self.MIN_TITLE_LENGTH:
            reasons.append('title_too_short')
        
        if len(post_data['content']) < self.MIN_CONTENT_LENGTH:
            reasons.append('content_too_short')
        
        # Check for promotional content
        if self._is_promotional(post_data['title'], post_data['content']):
            reasons.append('promotional_content')
        
        # Check for spam
        if self._is_spam(post_data['title'], post_data['content']):
            reasons.append('spam_content')
        
        # Check for deleted content
        if post_data['author'] == '[deleted]' and len(post_data['content']) < 50:
            reasons.append('deleted_content')
        
        is_valid = len(reasons) == 0
        return is_valid, reasons
    
    def _is_promotional(self, title, content):
        """Check if post contains promotional content."""
        text = f"{title} {content}".lower()
        return any(pattern.search(text) for pattern in self.compiled_promotional)
    
    def _is_spam(self, title, content):
        """Check if post contains spam indicators."""
        text = f"{title} {content}".lower()
        return any(pattern.search(text) for pattern in self.compiled_spam)
    
    @staticmethod
    def is_duplicate(text1, text2, threshold=0.85):
        """
        Check if two posts are duplicates using similarity ratio.
        
        Args:
            text1, text2: Post texts to compare
            threshold: Similarity ratio threshold (0-1)
        
        Returns:
            True if posts are similar enough to be duplicates
        """
        similarity = SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
        return similarity >= threshold
