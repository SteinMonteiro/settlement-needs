# Settlement Needs - Automated Service Gap Analysis

![Status](https://img.shields.io/badge/Phase-1-blue)
![Python](https://img.shields.io/badge/Python-3.12-green)
![Django](https://img.shields.io/badge/Django-5.1-green)
![License](https://img.shields.io/badge/License-MIT-blue)

## 🎯 Overview

**Settlement Needs** is a Django web application that automatically identifies gaps in settlement services for newcomers to Canada by collecting and analyzing Reddit posts from immigration communities. The system uses machine learning to categorize needs and alerts service providers about urgent, unmet demands.

### Mission
Provide government agencies, service providers, and community organizations with real-time, data-driven insights about settlement service demand and identify service gaps to improve newcomer integration.

## 🚀 Quick Start

### Option 1: Docker (Recommended)
```bash
# Clone and configure
git clone <repo>
cd settlement-needs
cp .env.example .env
# Edit .env with your Reddit API credentials

# Launch all services
docker-compose up

# Initialize database (new terminal)
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Access application
# Admin:  http://localhost:8000/admin
# Status: http://localhost:8000/ingestion/status/
```

### Option 2: Local Development
```bash
./dev-setup.sh

# Start in separate terminals:
python manage.py runserver
celery -A settlement_needs worker -l info
celery -A settlement_needs beat -l info
```

## 📋 Documentation

- **[PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)** - Complete project overview and roadmap
- **[SETUP_GUIDE.md](./SETUP_GUIDE.md)** - Detailed setup, API reference, and troubleshooting
- **[PHASE_1_README.md](./PHASE_1_README.md)** - Phase 1 specific documentation

## 🏗️ Project Architecture

### Phase 1: Data Ingestion Pipeline ✅ (Complete)
- Automated Reddit post collection from target communities
- Intelligent noise filtering (spam, promotional, low-quality content)
- Real-time data storage and tracking
- REST API for data access
- Admin interface for monitoring

### Phase 2-6 (Planned)
- **Phase 2**: ML Classification Engine (categorize needs)
- **Phase 3**: Enhanced Backend (database improvements)
- **Phase 4**: Alert System (caseworker notifications)
- **Phase 5**: Analytics Dashboard (visualizations & insights)
- **Phase 6**: Feedback Loop & Deployment (production ready)

## 🔧 Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | Django 5.1 (Python 3.12) |
| Database | PostgreSQL |
| Task Queue | Celery + Redis |
| Data Source | Reddit API (PRAW) |
| Deployment | Docker + Docker Compose |
| Testing | pytest, Django TestCase |

## 📊 Key Features (Phase 1)

✅ **Automated Data Collection**
- Monitors r/ImmigrationCanada, r/PersonalFinanceCanada, r/askTO
- Filters by relevant keywords (COPR, housing, employment, etc.)
- Configurable collection schedule (default: hourly)

✅ **Intelligent Filtering**
- Removes spam, promotional, and low-quality content
- Duplicate detection using similarity analysis
- Configurable noise detection rules

✅ **REST API**
- `/ingestion/status/` - System statistics
- `/ingestion/posts/` - List collected posts (paginated)
- `/ingestion/posts/<id>/` - Post details
- `/ingestion/logs/` - Job execution history

✅ **Admin Interface**
- Browse, filter, and search collected posts
- Review ingestion job logs
- Manual data classification (for future phases)

✅ **Background Jobs**
- Celery workers for async data collection
- Redis message broker for task queuing
- Celery Beat for scheduled hourly collection

## 🎯 Use Cases

### For Government Agencies
- Identify emerging settlement service gaps
- Allocate resources based on demand
- Measure service effectiveness

### For Service Providers
- Understand client needs in real-time
- Adjust offerings based on demand trends
- Collaborate on underserved areas

### For Community Organizations
- Track settlement challenges newcomers face
- Advocate for improved services
- Coordinate with other providers

## 🔑 Getting Started

### Prerequisites
- Python 3.12+
- PostgreSQL 12+
- Redis 6+
- Reddit API credentials (free - get at https://www.reddit.com/prefs/apps)

### Reddit API Setup (5 minutes)
1. Visit https://www.reddit.com/prefs/apps
2. Create a new "script" application
3. Copy Client ID, Client Secret, and create credentials
4. Add to `.env`:
   ```
   REDDIT_CLIENT_ID=your_id
   REDDIT_CLIENT_SECRET=your_secret
   REDDIT_USERNAME=your_username
   REDDIT_PASSWORD=your_password
   ```

### Full Setup Instructions
See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for detailed configuration.

## 📈 Example API Usage

### Get System Status
```bash
curl http://localhost:8000/ingestion/status/
```

### List Recent Posts
```bash
curl "http://localhost:8000/ingestion/posts/?page=1&subreddit=ImmigrationCanada"
```

### Get Post Details
```bash
curl http://localhost:8000/ingestion/posts/1/
```

## 📊 Sample Data

After running for a few hours, you'll have:
- **Posts Collected**: ~50-150 per hour
- **After Filtering**: ~40-120 valid posts per hour
- **Categories**: Housing, Employment, Health, Language, Visa, etc.
- **Data Points**: Title, content, author, engagement, sentiment, urgency

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific test module
python manage.py test ingestion

# With coverage report
coverage run --source='.' manage.py test
coverage report
```

## 📊 Database Schema

### RedditPost
Stores raw Reddit posts with filtering metadata
- `post_id`, `subreddit`, `author`, `title`, `content`
- `upvotes`, `comments_count`, `posted_at`
- `is_valid`, `is_noise`, `is_promotional`, `is_duplicate`

### IngestionLog
Tracks data collection job execution
- `task_id`, `status`, `started_at`, `completed_at`
- `posts_collected`, `posts_filtered`, `posts_saved`

## 🚀 Deployment

### Docker Production Build
```bash
docker build -t settlement-needs:latest .
docker tag settlement-needs:latest myregistry/settlement-needs:latest
docker push myregistry/settlement-needs:latest
```

### Environment Configuration
Set these for production:
```env
DEBUG=False
SECRET_KEY=<secure-random-key>
DB_PASSWORD=<strong-password>
ALLOWED_HOSTS=yourdomain.com
```

## 🔒 Security

- No Reddit credentials committed to repository
- Environment variables for all secrets
- PostgreSQL connection encryption recommended
- CSRF protection on all forms
- SQL injection prevention via ORM
- Input validation on all endpoints

## 📈 Monitoring

### Django Admin
- http://localhost:8000/admin
- View posts, logs, and system metrics
- Requires superuser login

### Celery Monitoring (Optional)
```bash
pip install flower
celery -A settlement_needs flower
# Visit http://localhost:5555
```

### Logs
```bash
tail -f logs/settlement_needs.log
```

## 🐛 Troubleshooting

**Redis not running?**
```bash
redis-server
```

**Database connection error?**
- Check PostgreSQL is running
- Verify credentials in `.env`

**No posts collected?**
- Verify Reddit credentials
- Check ingestion logs: `/ingestion/logs/`
- Review `logs/settlement_needs.log`

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for detailed troubleshooting.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📚 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [PRAW (Reddit API)](https://praw.readthedocs.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 📞 Support

- **Documentation**: [SETUP_GUIDE.md](./SETUP_GUIDE.md)
- **Issues**: Create a GitHub issue
- **Questions**: Use GitHub discussions

## 📄 License

MIT License - See LICENSE file for details

## 👥 Project Team

- **Created**: November 2024
- **Status**: Phase 1 Complete ✅
- **Next Phase**: ML Classification Engine

---

**Ready to help identify settlement service gaps? Start with the [SETUP_GUIDE.md](./SETUP_GUIDE.md)!**