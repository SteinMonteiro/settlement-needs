# Settlement Needs - Developer Quick Reference

## 🚀 Getting Started in 5 Minutes

### With Docker (Easiest)
```bash
cp .env.example .env
# Edit .env: add REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, etc.
docker-compose up
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
# Go to http://localhost:8000/admin
```

### Locally (Advanced)
```bash
./dev-setup.sh
# Follow the printed instructions to start Django, Celery, and Celery Beat
```

---

## 📚 Key Files to Know

| File | Purpose |
|------|---------|
| `settlement_needs/settings.py` | Django configuration, database, Celery setup |
| `ingestion/models.py` | RedditPost and IngestionLog models |
| `ingestion/tasks.py` | Main Celery task: `ingest_reddit_posts` |
| `ingestion/filters.py` | NoiseFilter class for spam/promotional removal |
| `ingestion/views.py` | REST API endpoints |
| `ingestion/admin.py` | Django admin interface configuration |
| `.env` | Environment variables (Reddit creds, DB, etc.) |

---

## 🔄 Data Flow

```
Reddit API
    ↓
PRAW (Python Reddit API)
    ↓
collect_posts_from_subreddit() → Filter by keywords
    ↓
is_relevant_post() → Check TARGET_KEYWORDS
    ↓
NoiseFilter.filter_post() → Remove spam/promotional/low-quality
    ↓
RedditPost.objects.update_or_create() → Save to database
    ↓
Django Admin / REST API → User access
```

---

## 💾 Database Models

### RedditPost
```python
class RedditPost(models.Model):
    post_id = CharField(unique=True)          # Reddit ID
    subreddit = CharField()                   # Source subreddit
    author = CharField()                      # Post author
    title = CharField(max_length=500)         # Post title
    content = TextField()                     # Post body
    url = URLField(unique=True)               # Reddit link
    upvotes = IntegerField()                  # Vote count
    comments_count = IntegerField()           # Comment count
    posted_at = DateTimeField()               # When posted
    is_valid = BooleanField(default=True)     # Passed filters
    is_noise = BooleanField(default=False)    # Flagged as noise
    noise_reason = CharField()                # Why filtered
    is_promotional = BooleanField()           # Ad/promotional
    is_duplicate = BooleanField()             # Duplicate content
```

### IngestionLog
```python
class IngestionLog(models.Model):
    task_id = CharField(unique=True)          # Celery task ID
    status = CharField(choices=...)           # pending/running/completed/failed
    started_at = DateTimeField()              # Job start
    completed_at = DateTimeField()            # Job end
    posts_collected = IntegerField()          # Raw posts fetched
    posts_filtered = IntegerField()           # Posts removed
    posts_saved = IntegerField()              # Posts stored
    error_message = TextField()               # Error details
```

---

## 🔧 Common Commands

### Django Management
```bash
python manage.py migrate                  # Apply database migrations
python manage.py makemigrations          # Create new migrations
python manage.py createsuperuser         # Create admin user
python manage.py runserver               # Start dev server (port 8000)
python manage.py shell                   # Interactive Python shell
python manage.py test                    # Run tests
python manage.py collectstatic           # Gather static files
```

### Celery
```bash
celery -A settlement_needs worker -l info           # Start worker
celery -A settlement_needs beat -l info             # Start scheduler
celery -A settlement_needs inspect active           # View active tasks
celery -A settlement_needs inspect reserved        # View reserved tasks
celery -A settlement_needs purge                    # Clear task queue
celery -A settlement_needs flower                   # Start monitoring (port 5555)
```

### Database
```bash
psql -U postgres -d settlement_needs    # Connect to database
python manage.py dbshell               # Django database shell
```

---

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app
python manage.py test ingestion

# Run specific test class
python manage.py test ingestion.tests.NoiseFilterTest

# Run with verbose output
python manage.py test -v 2

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Open htmlcov/index.html
```

### Test Files
- `ingestion/tests.py` - Tests for models and filters

---

## 🐛 Debug Tips

### Check recent posts
```bash
python manage.py shell
>>> from ingestion.models import RedditPost
>>> posts = RedditPost.objects.filter(is_valid=True).order_by('-posted_at')[:5]
>>> for p in posts: print(f"{p.subreddit}: {p.title}")
```

### Check ingestion logs
```bash
python manage.py shell
>>> from ingestion.models import IngestionLog
>>> logs = IngestionLog.objects.order_by('-completed_at')[:5]
>>> for log in logs: print(f"{log.task_id}: {log.status} ({log.posts_saved} saved)")
```

### Trigger ingestion manually
```bash
python manage.py shell
>>> from ingestion.tasks import ingest_reddit_posts
>>> result = ingest_reddit_posts.apply_async()
>>> print(result.get())  # Wait for result
```

### View Celery logs
```bash
tail -f logs/settlement_needs.log
```

### Check Redis
```bash
redis-cli ping              # Should return "PONG"
redis-cli info              # Server info
redis-cli keys '*'          # List all keys
redis-cli flush all         # Clear all data
```

---

## 🛠️ Common Customizations

### Change Data Collection Frequency
Edit `.env`:
```
# Every 30 minutes (1800 seconds)
DATA_INGESTION_INTERVAL=1800

# Every 6 hours (21600 seconds)
DATA_INGESTION_INTERVAL=21600
```

### Add Target Subreddit
Edit `ingestion/tasks.py`:
```python
TARGET_SUBREDDITS = [
    'ImmigrationCanada',
    'PersonalFinanceCanada',
    'askTO',
    'NewHere',  # Add new subreddit
]
```

### Add Target Keyword
Edit `ingestion/tasks.py`:
```python
TARGET_KEYWORDS = [
    'new to canada',
    'copr',
    'settlement',
    # Add keywords...
]
```

### Adjust Noise Filter Rules
Edit `ingestion/filters.py`:
```python
class NoiseFilter:
    # Modify PROMOTIONAL_PATTERNS, SPAM_PATTERNS, etc.
    MIN_TITLE_LENGTH = 10      # Change thresholds
    MIN_CONTENT_LENGTH = 20
```

---

## 📊 API Examples

### Check System Status
```bash
curl http://localhost:8000/ingestion/status/ | python -m json.tool
```

### List Posts (Page 1)
```bash
curl "http://localhost:8000/ingestion/posts/?page=1" | python -m json.tool
```

### Filter by Subreddit
```bash
curl "http://localhost:8000/ingestion/posts/?subreddit=ImmigrationCanada" | python -m json.tool
```

### Get Post Details
```bash
curl http://localhost:8000/ingestion/posts/1/ | python -m json.tool
```

### Check Ingestion Logs
```bash
curl "http://localhost:8000/ingestion/logs/?status=completed" | python -m json.tool
```

---

## 🚨 Troubleshooting

| Problem | Solution |
|---------|----------|
| Redis connection error | `redis-server` or `brew services start redis` |
| Database error | Check `.env` DB settings, ensure PostgreSQL is running |
| Reddit API auth fails | Verify `.env` credentials at reddit.com/prefs/apps |
| No posts collected | Check target keywords match posts, review logs |
| Celery tasks stuck | Restart worker, check Redis, clear queue with `celery purge` |
| Django admin not loading | Check migrations: `python manage.py migrate` |

---

## 📁 Project Structure

```
settlement-needs/
├── settlement_needs/          # Main Django project
│   ├── settings.py           # ⭐ Start here for config
│   ├── urls.py               # URL routing
│   ├── celery.py             # Celery app config
│   └── __init__.py
├── ingestion/                 # Data collection app
│   ├── models.py             # ⭐ Database models
│   ├── tasks.py              # ⭐ Main collection logic
│   ├── filters.py            # Spam/noise filters
│   ├── views.py              # API endpoints
│   ├── admin.py              # Admin interface
│   ├── tests.py              # Unit tests
│   └── migrations/           # Database migrations
├── templates/                # HTML templates
├── static/                   # CSS, JS, images
├── logs/                     # Application logs
├── manage.py                 # Django CLI
├── requirements.txt          # Python packages
├── .env                      # Secrets (don't commit!)
├── .env.example              # Template (safe to commit)
├── docker-compose.yml        # Container setup
├── Dockerfile                # Container image
├── dev-setup.sh              # Local dev setup script
└── README.md                 # Project overview
```

---

## 🔐 Security Reminders

⚠️ **NEVER COMMIT THESE:**
- `.env` file (use `.env.example` as template)
- Database passwords
- Reddit API secrets
- Email credentials

✅ **ALWAYS:**
- Use environment variables for secrets
- Keep dependencies updated: `pip install --upgrade -r requirements.txt`
- Review security logs regularly
- Use strong passwords

---

## 📞 Help Resources

- **README.md** - Project overview
- **SETUP_GUIDE.md** - Detailed setup and API reference
- **PROJECT_SUMMARY.md** - Architecture and roadmap
- **PHASE_1_README.md** - Phase 1 specific docs
- **Django Docs** - https://docs.djangoproject.com/
- **Celery Docs** - https://docs.celeryproject.org/

---

## ✨ What's Next?

### Phase 1 (Current) ✅
- [x] Reddit data collection
- [x] Noise filtering
- [x] Database storage
- [x] API endpoints
- [x] Admin interface

### Phase 2 (Coming Soon)
- [ ] ML classification engine
- [ ] Service category taxonomy
- [ ] Confidence scoring

### Phase 3+
- [ ] Advanced analytics
- [ ] Caseworker alerts
- [ ] Policy dashboard
- [ ] Model retraining UI
- [ ] Production deployment

---

**Happy coding! 🚀**
