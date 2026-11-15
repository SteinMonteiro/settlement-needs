# Settlement Needs - Complete Setup & Deployment Guide

## 📋 Quick Start

### Option 1: Docker (Recommended - Easiest)

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with your Reddit API credentials

# 2. Start all services
docker-compose up

# 3. Initialize database (in another terminal)
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# 4. Access the application
# Admin: http://localhost:8000/admin
# API Status: http://localhost:8000/ingestion/status/
```

### Option 2: Local Development

```bash
# 1. Prerequisites
python --version  # Should be 3.12+
redis-server --version
psql --version  # Should be installed

# 2. Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 4. Start Redis
redis-server

# 5. Database setup
python manage.py migrate
python manage.py createsuperuser

# 6. Run services (each in separate terminal)
python manage.py runserver
celery -A settlement_needs worker -l info
celery -A settlement_needs beat -l info
```

## 🔧 Reddit API Setup (Required for Data Collection)

### Getting Reddit Credentials

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill out the form:
   - **Name**: Settlement Needs
   - **App type**: Select "script"
   - **Description**: Data collection for settlement needs analysis
   - **Redirect URI**: http://localhost (can be any valid URI)
4. Click "Create app"
5. You'll see your credentials:
   - **Client ID**: Under your app name (14-character string)
   - **Client Secret**: The secret code shown
6. Add these to your `.env`:
   ```
   REDDIT_CLIENT_ID=your_client_id_here
   REDDIT_CLIENT_SECRET=your_secret_here
   REDDIT_USERNAME=your_reddit_username
   REDDIT_PASSWORD=your_reddit_password
   REDDIT_USER_AGENT=SettlementNeeds/1.0 (by your_username)
   ```

## 📦 Project Structure

```
settlement-needs/
│
├── settlement_needs/          # Main Django project settings
│   ├── settings.py           # Django configuration
│   ├── urls.py               # Root URL routing
│   ├── wsgi.py               # WSGI application
│   ├── asgi.py               # ASGI application
│   ├── celery.py             # Celery configuration
│   └── __init__.py
│
├── ingestion/                 # Core data ingestion app
│   ├── models.py             # RedditPost, IngestionLog models
│   ├── tasks.py              # Celery background tasks
│   ├── filters.py            # NoiseFilter implementation
│   ├── views.py              # API endpoints
│   ├── admin.py              # Django admin interface
│   ├── urls.py               # App URL routing
│   ├── apps.py               # App configuration
│   ├── tests.py              # Unit tests
│   └── migrations/
│
├── templates/                # HTML templates (future use)
├── static/                   # Static files (CSS, JS)
├── logs/                     # Application logs
├── media/                    # Media files
│
├── docker-compose.yml        # Multi-container orchestration
├── Dockerfile                # Container image definition
├── init.sh                   # Initialization script
├── manage.py                 # Django management command
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variable template
├── PHASE_1_README.md         # Phase 1 documentation
└── SETUP_GUIDE.md            # This file
```

## 🚀 API Reference

### Endpoints

#### 1. GET `/ingestion/status/`
Get real-time statistics and recent ingestion job status.

**Response:**
```json
{
  "total_posts": 1234,
  "valid_posts": 980,
  "noise_posts": 200,
  "promotional_posts": 54,
  "recent_logs": [
    {
      "task_id": "abc123def456",
      "status": "completed",
      "posts_collected": 150,
      "posts_filtered": 30,
      "posts_saved": 120,
      "started_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### 2. GET `/ingestion/posts/`
List all collected Reddit posts with filtering and pagination.

**Query Parameters:**
- `subreddit`: Filter by subreddit (e.g., `?subreddit=ImmigrationCanada`)
- `is_valid`: Filter by validity (e.g., `?is_valid=true`)
- `page`: Page number (default: 1)

**Response:**
```json
{
  "count": 980,
  "page": 1,
  "total_pages": 49,
  "results": [
    {
      "id": 1,
      "title": "Help with settlement in Canada",
      "subreddit": "ImmigrationCanada",
      "author": "john_doe",
      "posted_at": "2024-01-15T10:15:00Z",
      "upvotes": 5,
      "comments_count": 2,
      "is_valid": true,
      "is_noise": false,
      "is_promotional": false
    }
  ]
}
```

#### 3. GET `/ingestion/posts/<id>/`
Get detailed information about a specific post.

**Response:**
```json
{
  "id": 1,
  "post_id": "abc123",
  "title": "Help with settlement in Canada",
  "content": "I just got my COPR and need advice on housing...",
  "subreddit": "ImmigrationCanada",
  "author": "john_doe",
  "url": "https://reddit.com/r/ImmigrationCanada/comments/abc123",
  "posted_at": "2024-01-15T10:15:00Z",
  "upvotes": 5,
  "comments_count": 2,
  "is_valid": true,
  "is_noise": false,
  "noise_reason": null,
  "is_promotional": false,
  "is_duplicate": false,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### 4. GET `/ingestion/logs/`
List ingestion job execution logs.

**Query Parameters:**
- `status`: Filter by status (pending, running, completed, failed)
- `page`: Page number

**Response:**
```json
{
  "count": 42,
  "page": 1,
  "total_pages": 3,
  "results": [
    {
      "task_id": "abc123def456",
      "status": "completed",
      "started_at": "2024-01-15T10:30:00Z",
      "completed_at": "2024-01-15T10:35:12Z",
      "posts_collected": 150,
      "posts_filtered": 30,
      "posts_saved": 120,
      "error_message": null
    }
  ]
}
```

## 📊 Data Models

### RedditPost

| Field | Type | Description |
|-------|------|-------------|
| `id` | Primary Key | Auto-generated ID |
| `post_id` | String (unique) | Reddit post ID |
| `subreddit` | String | Source subreddit name |
| `author` | String | Post author username |
| `title` | String (500 chars) | Post title |
| `content` | Text | Full post content |
| `url` | URL (unique) | Direct link to Reddit post |
| `upvotes` | Integer | Reddit upvote count |
| `comments_count` | Integer | Comment count |
| `posted_at` | DateTime | When post was created on Reddit |
| `created_at` | DateTime | When record was created |
| `updated_at` | DateTime | Last update timestamp |
| `is_valid` | Boolean | Passed all filters (indexed) |
| `is_noise` | Boolean | Flagged as low-quality/irrelevant |
| `noise_reason` | String | Explanation of noise flag |
| `is_promotional` | Boolean | Flagged as promotional/spam |
| `is_duplicate` | Boolean | Flagged as duplicate content |

### IngestionLog

| Field | Type | Description |
|-------|------|-------------|
| `id` | Primary Key | Auto-generated ID |
| `task_id` | String (unique) | Celery task ID |
| `status` | Choice | pending, running, completed, failed |
| `started_at` | DateTime | Job start time |
| `completed_at` | DateTime | Job completion time |
| `posts_collected` | Integer | Raw posts fetched from Reddit |
| `posts_filtered` | Integer | Posts removed by filters |
| `posts_saved` | Integer | Posts successfully stored |
| `error_message` | Text | Error details if failed |

## 🔍 Noise Filtering Logic

The system automatically removes posts that don't meet quality standards:

### 1. Low-Quality Posts
- Title < 10 characters
- Content < 20 characters

### 2. Promotional Content
- Contains URLs (www., http://, https://)
- Promotional keywords: "visit", "check out", "click here", "sign up"
- Ad indicators: "advertisement", "sponsored"
- Direct contact requests: "dm me", "message me"

### 3. Spam & Suspicious Content
- Crypto/financial spam: "crypto", "bitcoin", "forex", "gambling"
- High-pressure sales: "make money fast", "easy cash", "act fast"
- Work-from-home scams: "work from home"

### 4. Deleted/Invalid Content
- Author is "[deleted]" with minimal content

## ⏰ Scheduling Configuration

Ingestion runs automatically on a schedule managed by **Celery Beat**.

### Default Schedule
- **Frequency**: Every 1 hour
- **Task**: `ingestion.tasks.ingest_reddit_posts`
- **Configuration**: `.env` → `DATA_INGESTION_INTERVAL` (in seconds)

### Adjust Frequency
Edit `.env`:
```
# Every 30 minutes
DATA_INGESTION_INTERVAL=1800

# Every 2 hours
DATA_INGESTION_INTERVAL=7200

# Every 6 hours
DATA_INGESTION_INTERVAL=21600
```

Restart Celery Beat for changes to take effect.

## 🧪 Testing

### Run All Tests
```bash
python manage.py test
```

### Run Tests for Specific App
```bash
python manage.py test ingestion
```

### Run with Coverage
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Manual Testing

#### Test Ingestion Task
```bash
python manage.py shell
>>> from ingestion.tasks import ingest_reddit_posts
>>> result = ingest_reddit_posts.apply_async()
>>> result.get()  # Wait for result
{'status': 'success', 'posts_collected': 150, ...}
```

#### Check Stored Posts
```bash
python manage.py shell
>>> from ingestion.models import RedditPost
>>> RedditPost.objects.count()
980
>>> RedditPost.objects.filter(is_valid=True).count()
900
>>> RedditPost.objects.filter(is_noise=True).count()
50
```

## 🎯 Monitoring

### Django Admin Interface
1. Visit http://localhost:8000/admin
2. Login with superuser credentials
3. Browse:
   - **Reddit Posts**: View, filter, and search collected posts
   - **Ingestion Logs**: Monitor job execution history

### Command Line
```bash
# Recent posts
python manage.py shell << EOF
from ingestion.models import RedditPost
posts = RedditPost.objects.filter(is_valid=True).order_by('-posted_at')[:10]
for p in posts:
    print(f"{p.subreddit}: {p.title}")
EOF

# Ingestion stats
python manage.py shell << EOF
from ingestion.models import IngestionLog
logs = IngestionLog.objects.filter(status='completed').order_by('-completed_at')[:5]
for log in logs:
    print(f"{log.task_id}: {log.posts_saved} saved ({log.posts_filtered} filtered)")
EOF
```

### Optional: Flower (Celery Monitor)
```bash
pip install flower
celery -A settlement_needs flower
# Visit http://localhost:5555
```

## 🐛 Troubleshooting

### Issue: Database Connection Error
```
django.db.utils.OperationalError: could not connect to server
```
**Solution:**
- Ensure PostgreSQL is running: `psql -U postgres`
- Check credentials in `.env`
- For Docker: `docker-compose ps` (verify db service is running)

### Issue: Redis Connection Error
```
ConnectionError: Error -1 connecting to localhost:6379
```
**Solution:**
- Ensure Redis is running: `redis-cli ping`
- Check `REDIS_URL` in `.env`
- For Docker: `docker-compose logs redis`

### Issue: Reddit API Authentication Failed
```
PRAW exception: Received 401 HTTP response
```
**Solution:**
- Verify credentials at https://www.reddit.com/prefs/apps
- Ensure user_agent format is correct: `AppName/1.0 (by reddit_username)`
- Check `.env` for typos

### Issue: Celery Tasks Not Running
```
No tasks in queue
```
**Solution:**
- Verify Celery worker is running: `celery -A settlement_needs worker -l info`
- Check Celery Beat is running: `celery -A settlement_needs beat`
- Review logs for errors: `tail -f logs/settlement_needs.log`

### Issue: No Posts Being Collected
**Debug Steps:**
1. Check if target keywords are matching:
   ```bash
   python manage.py shell
   >>> from ingestion.tasks import TARGET_KEYWORDS
   >>> print(TARGET_KEYWORDS)
   ```
2. Manually test Reddit connection:
   ```bash
   python manage.py shell
   >>> from ingestion.tasks import get_reddit_client
   >>> reddit = get_reddit_client()
   >>> sub = reddit.subreddit('ImmigrationCanada')
   >>> print(sub.display_name)
   ```
3. Check logs: `tail -f logs/settlement_needs.log`

## 📈 Performance Tips

### Database Optimization
```bash
# Create indexes for faster queries
python manage.py sqlsequencereset ingestion | python manage.py dbshell

# Analyze query performance
django.db.connection.queries  # In shell, see query count
```

### Celery Optimization
Adjust concurrency in `.env`:
```
# Increase worker processes for better parallelism
CELERY_WORKER_CONCURRENCY=4
```

### Pagination
Default page size is 20 posts. Adjust in [views.py](/ingestion/views.py):
```python
paginator = Paginator(posts, 20)  # Change 20 to desired page size
```

## 🔒 Security Considerations

### Environment Variables
- Never commit `.env` to repository
- `.env.example` is safe to share (no secrets)
- Use strong database passwords in production
- Rotate Reddit API credentials periodically

### Database
- Use PostgreSQL with SSL in production
- Regular backups: `pg_dump settlement_needs > backup.sql`
- Restrict database access to app servers only

### API
- Add rate limiting in production
- Implement authentication for admin endpoints
- Use HTTPS only in production

## 🚀 Deployment (Production)

### Using Docker
```bash
# Build image
docker build -t settlement-needs:latest .

# Push to registry (e.g., Docker Hub)
docker tag settlement-needs:latest username/settlement-needs:latest
docker push username/settlement-needs:latest

# Deploy to cloud (e.g., AWS ECS, Google Cloud Run, etc.)
```

### Environment Setup
```bash
# Production .env
DEBUG=False
SECRET_KEY=<generate-secure-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_PASSWORD=<strong-password>
REDDIT_CLIENT_ID=<your-id>
REDDIT_CLIENT_SECRET=<your-secret>
```

### Database Migrations
```bash
python manage.py migrate
```

### Static Files
```bash
python manage.py collectstatic --noinput
```

## 📚 Next Steps (Phase 2+)

- **Phase 2**: ML classification engine (SVM, NLP)
- **Phase 3**: Dashboard and analytics
- **Phase 4**: Alert system for caseworkers
- **Phase 5**: Visualization and gap analysis
- **Phase 6**: Model retraining UI and production deployment

---

**For questions or issues, open an issue on GitHub or contact the development team.**
