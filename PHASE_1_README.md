# Settlement Needs - Phase 1: Data Ingestion Pipeline

## Project Overview

This Django application collects Reddit posts about settlement needs from newcomers to Canada, filters out noise, and stores relevant data for downstream analysis. This is **Phase 1** of a multi-phase project to identify gaps in settlement services.

### Phase 1 Goals
- ✅ Automated Reddit data collection from targeted subreddits
- ✅ Noise reduction filtering (duplicates, promotional content, spam)
- ✅ Database storage of raw posts and metadata
- ✅ Background job scheduling with Celery + Redis
- ✅ Admin interface for monitoring and triage

### Target Subreddits
- r/ImmigrationCanada
- r/PersonalFinanceCanada
- r/askTO

### Target Keywords
- "new to canada"
- "copr"
- "settlement"
- "housing"
- "employment"
- "health"
- "language"
- "visa"
- "immigration"

## Setup Instructions

### Prerequisites
- Python 3.12+
- PostgreSQL 12+
- Redis 6+

### 1. Clone and Install Dependencies

```bash
cd settlement-needs
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example .env file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with:
- **Database credentials** (PostgreSQL)
- **Reddit API credentials** (PRAW):
  - Get these from https://www.reddit.com/prefs/apps
  - Create a "script" app to get client_id and client_secret
- **Redis URL** (if not localhost:6379)

### 3. Database Setup

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Start Services

#### In separate terminals:

**Terminal 1: Django Development Server**
```bash
python manage.py runserver
```

**Terminal 2: Celery Worker**
```bash
celery -A settlement_needs worker -l info
```

**Terminal 3: Celery Beat (Scheduler)**
```bash
celery -A settlement_needs beat -l info
```

### 5. Access the Application

- **Django Admin**: http://localhost:8000/admin
- **API Status**: http://localhost:8000/ingestion/status/
- **Posts List**: http://localhost:8000/ingestion/posts/
- **Ingestion Logs**: http://localhost:8000/ingestion/logs/

## API Endpoints

### GET `/ingestion/status/`
Returns summary statistics and recent ingestion job logs.

```json
{
  "total_posts": 1234,
  "valid_posts": 980,
  "noise_posts": 200,
  "promotional_posts": 54,
  "recent_logs": [...]
}
```

### GET `/ingestion/posts/`
List all collected posts with pagination and filtering.

**Query Parameters:**
- `subreddit`: Filter by subreddit name
- `is_valid`: Filter by validity (true/false)
- `page`: Page number (default: 1)

### GET `/ingestion/posts/<id>/`
Get detailed information about a specific post.

### GET `/ingestion/logs/`
List all ingestion job logs with filtering.

**Query Parameters:**
- `status`: Filter by job status (pending, running, completed, failed)
- `page`: Page number

## Data Models

### RedditPost
Stores raw Reddit posts collected from target subreddits.

**Fields:**
- `post_id`: Unique Reddit post ID
- `subreddit`: Source subreddit
- `author`: Post author username
- `title`, `content`: Post text
- `url`: Direct link to post
- `upvotes`, `comments_count`: Engagement metrics
- `posted_at`: When post was created on Reddit
- `created_at`, `updated_at`: Database timestamps
- `is_valid`: Whether post passed filtering
- `is_noise`: Flagged as irrelevant/low-quality
- `is_promotional`: Flagged as promotional
- `is_duplicate`: Flagged as duplicate content
- `noise_reason`: Explanation of why filtered

### IngestionLog
Tracks each ingestion job's execution and results.

**Fields:**
- `task_id`: Unique Celery task ID
- `status`: pending, running, completed, or failed
- `started_at`, `completed_at`: Execution timeline
- `posts_collected`: Raw posts fetched
- `posts_filtered`: Posts removed by filters
- `posts_saved`: Posts successfully stored
- `error_message`: Error details if failed

## Noise Filtering Strategy

The `NoiseFilter` class in `ingestion/filters.py` removes posts that:

1. **Low-Quality Content**
   - Title < 10 characters
   - Content < 20 characters

2. **Promotional Content**
   - URLs (www., https://)
   - Call-to-action phrases ("visit", "click here", "sign up")
   - Advertisement indicators

3. **Spam/Suspicious Content**
   - Crypto/forex/gambling keywords
   - "Make money fast" type language
   - High-pressure sales tactics

4. **Deleted Content**
   - Author is "[deleted]" with minimal content

## Scheduling

Ingestion runs automatically every hour (configurable via `DATA_INGESTION_INTERVAL` in `.env`).

The schedule is managed by Celery Beat:
- Reads from `CELERY_BEAT_SCHEDULE` in `settings.py`
- Executes `ingestion.tasks.ingest_reddit_posts`
- Results stored in IngestionLog table

## Monitoring

### Django Admin Interface
1. Navigate to http://localhost:8000/admin
2. View "Reddit Posts" and "Ingestion Logs"
3. Search, filter, and review ingestion results

### Celery Monitoring (Optional)
Install Flower for visual monitoring:
```bash
pip install flower
celery -A settlement_needs flower
# Visit http://localhost:5555
```

## Testing the Ingestion Pipeline

### Manual Trigger
Run ingestion immediately (without waiting for scheduler):

```bash
python manage.py shell
>>> from ingestion.tasks import ingest_reddit_posts
>>> result = ingest_reddit_posts.apply_async()
>>> print(result.get())
```

### View Results
```bash
python manage.py shell
>>> from ingestion.models import RedditPost, IngestionLog
>>> RedditPost.objects.count()
>>> IngestionLog.objects.latest('started_at')
```

## Next Steps (Phase 2+)

Once Phase 1 is stable, we'll build:
- **Phase 2**: ML classification engine for categorizing needs
- **Phase 3**: Dashboard and advanced analytics
- **Phase 4**: Alert system for caseworkers
- **Phase 5**: Visualization and gap analysis
- **Phase 6**: Model retraining UI and deployment

## Troubleshooting

### Redis Connection Error
```
Error: Cannot connect to Redis
```
Ensure Redis is running:
```bash
redis-server  # or 'brew services start redis' on macOS
```

### Reddit API Authentication Failed
- Verify credentials in `.env` are correct
- Ensure Reddit app is created at https://www.reddit.com/prefs/apps
- Check user_agent is properly formatted

### Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Project Structure

```
settlement-needs/
├── settlement_needs/          # Main Django project
│   ├── settings.py           # Configuration
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI app
│   ├── celery.py            # Celery config
│   └── __init__.py
├── ingestion/                 # Data ingestion app
│   ├── models.py            # RedditPost, IngestionLog
│   ├── tasks.py             # Celery tasks
│   ├── filters.py           # NoiseFilter class
│   ├── views.py             # API endpoints
│   ├── admin.py             # Django admin
│   ├── urls.py              # App URLs
│   └── migrations/
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

## License

MIT License - Settlement Needs Project

## Contributing

This is an active development project. Contributions welcome!

1. Create a feature branch
2. Make your changes
3. Submit a pull request

---

**Built with Django 5.1, Celery 5.3, and PRAW 7.7**
