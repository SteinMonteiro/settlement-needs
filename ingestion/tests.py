from django.test import TestCase
from django.utils import timezone
from ingestion.models import RedditPost, IngestionLog
from ingestion.filters import NoiseFilter


class RedditPostModelTest(TestCase):
    def setUp(self):
        self.post = RedditPost.objects.create(
            post_id='test123',
            subreddit='ImmigrationCanada',
            author='testuser',
            title='Help with settlement in Canada',
            content='I just got my COPR and need advice on where to live.',
            url='https://reddit.com/r/ImmigrationCanada/comments/test123',
            upvotes=5,
            comments_count=2,
            posted_at=timezone.now(),
        )
    
    def test_post_creation(self):
        self.assertEqual(self.post.post_id, 'test123')
        self.assertEqual(self.post.subreddit, 'ImmigrationCanada')
        self.assertTrue(self.post.is_valid)
        self.assertFalse(self.post.is_noise)
    
    def test_post_str_representation(self):
        self.assertIn('Help with settlement', str(self.post))
    
    def test_post_ordering(self):
        newer_post = RedditPost.objects.create(
            post_id='test456',
            subreddit='ImmigrationCanada',
            author='testuser2',
            title='Another settlement post',
            content='Need help with housing.',
            url='https://reddit.com/r/ImmigrationCanada/comments/test456',
            posted_at=timezone.now(),
        )
        posts = RedditPost.objects.all()
        self.assertEqual(posts.first().post_id, 'test456')  # Newest first


class IngestionLogModelTest(TestCase):
    def test_log_creation(self):
        log = IngestionLog.objects.create(
            task_id='celery-task-123',
            status='completed',
            posts_collected=100,
            posts_filtered=20,
            posts_saved=80,
        )
        self.assertEqual(log.task_id, 'celery-task-123')
        self.assertEqual(log.status, 'completed')


class NoiseFilterTest(TestCase):
    def setUp(self):
        self.filter = NoiseFilter()
    
    def test_filter_valid_post(self):
        post_data = {
            'title': 'Help with settlement in Canada',
            'content': 'I just got my COPR and need advice on housing and employment.',
            'author': 'testuser',
            'post_id': 'test123',
            'subreddit': 'ImmigrationCanada',
            'url': 'https://reddit.com/test',
            'upvotes': 5,
            'comments_count': 2,
            'posted_at': timezone.now(),
        }
        is_valid, reasons = self.filter.filter_post(post_data)
        self.assertTrue(is_valid)
        self.assertEqual(len(reasons), 0)
    
    def test_filter_short_title(self):
        post_data = {
            'title': 'Help',
            'content': 'This is a longer piece of content about settlement needs.',
            'author': 'testuser',
            'post_id': 'test123',
            'subreddit': 'ImmigrationCanada',
            'url': 'https://reddit.com/test',
            'upvotes': 5,
            'comments_count': 2,
            'posted_at': timezone.now(),
        }
        is_valid, reasons = self.filter.filter_post(post_data)
        self.assertFalse(is_valid)
        self.assertIn('title_too_short', reasons)
    
    def test_filter_promotional_content(self):
        post_data = {
            'title': 'Check out this amazing settlement service',
            'content': 'Visit our website at www.example.com and sign up today!',
            'author': 'testuser',
            'post_id': 'test123',
            'subreddit': 'ImmigrationCanada',
            'url': 'https://reddit.com/test',
            'upvotes': 5,
            'comments_count': 2,
            'posted_at': timezone.now(),
        }
        is_valid, reasons = self.filter.filter_post(post_data)
        self.assertFalse(is_valid)
        self.assertIn('promotional_content', reasons)
    
    def test_filter_spam_content(self):
        post_data = {
            'title': 'Make money fast with crypto',
            'content': 'Earn easy cash with our bitcoin scheme. Act fast, limited time offer!',
            'author': 'testuser',
            'post_id': 'test123',
            'subreddit': 'ImmigrationCanada',
            'url': 'https://reddit.com/test',
            'upvotes': 5,
            'comments_count': 2,
            'posted_at': timezone.now(),
        }
        is_valid, reasons = self.filter.filter_post(post_data)
        self.assertFalse(is_valid)
        self.assertIn('spam_content', reasons)
    
    def test_duplicate_detection(self):
        text1 = "I just arrived in Canada and need help with housing and employment"
        text2 = "I just arrived in Canada and need help with housing and employment"
        is_duplicate = NoiseFilter.is_duplicate(text1, text2)
        self.assertTrue(is_duplicate)
    
    def test_not_duplicate(self):
        text1 = "I need help with housing"
        text2 = "The weather in Canada is cold"
        is_duplicate = NoiseFilter.is_duplicate(text1, text2)
        self.assertFalse(is_duplicate)
