# Settlement Needs - Documentation Index

## 📍 Start Here

**New to the project?** Start with one of these based on your role:

### 👨‍💼 For Project Managers
→ Read **[PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)**
- Complete project vision and roadmap
- All 6 phases explained
- Timeline and dependencies
- Technical architecture overview

### 👨‍💻 For Developers (Setup)
→ Read **[SETUP_GUIDE.md](./SETUP_GUIDE.md)** then **[DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md)**
- Complete setup instructions (Docker & Local)
- API endpoint reference
- Database schema
- Common commands
- Troubleshooting guide

### ⚡ For Developers (Quick Start)
→ Read **[DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md)**
- 5-minute quick start
- Key files to know
- Common commands
- Database models
- Quick debugging tips

### 🚀 For DevOps/Infrastructure
→ Read **[SETUP_GUIDE.md](./SETUP_GUIDE.md)** - Deployment section
- Docker containerization
- docker-compose setup
- Production configuration
- Scaling recommendations

### 📖 For Phase 1 Deep Dive
→ Read **[PHASE_1_README.md](./PHASE_1_README.md)**
- Phase 1 goals and deliverables
- Noise filtering strategy
- Detailed feature explanations
- Testing and monitoring

---

## 📚 Documentation Files

### Core Documentation

| File | Purpose | Audience |
|------|---------|----------|
| [README.md](./README.md) | Project overview & quick start | Everyone |
| [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md) | Complete vision, roadmap, and architecture | PMs, Architects, Leads |
| [SETUP_GUIDE.md](./SETUP_GUIDE.md) | Detailed setup, API reference, troubleshooting | Developers, DevOps |
| [DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md) | Quick reference for common tasks | Developers |
| [PHASE_1_README.md](./PHASE_1_README.md) | Phase 1 specific features and details | Developers, PMs |

### Quick Navigation

- **Getting Started** → [README.md](./README.md) → 5-minute overview
- **Full Setup** → [SETUP_GUIDE.md](./SETUP_GUIDE.md) → Step-by-step guide
- **Development** → [DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md) → Common tasks
- **Understanding the Project** → [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md) → Full picture
- **Phase 1 Details** → [PHASE_1_README.md](./PHASE_1_README.md) → Current phase

---

## 📁 Project Structure

```
settlement-needs/                    # Root project directory
│
├── 📄 Core Documentation
│   ├── README.md                   # Project overview (start here!)
│   ├── PROJECT_SUMMARY.md          # Complete roadmap & architecture
│   ├── SETUP_GUIDE.md              # Detailed setup guide
│   ├── DEVELOPER_GUIDE.md          # Quick reference for developers
│   ├── PHASE_1_README.md           # Phase 1 specific guide
│   └── INDEX.md                    # This file
│
├── 🐍 Django Project Core
│   ├── manage.py                   # Django CLI
│   ├── requirements.txt            # Python dependencies
│   │
│   └── settlement_needs/           # Main Django project
│       ├── settings.py             # Django configuration
│       ├── urls.py                 # Root URL routing
│       ├── wsgi.py                 # WSGI application
│       ├── asgi.py                 # ASGI application
│       ├── celery.py               # Celery setup
│       └── __init__.py
│
├── 📦 Ingestion App (Phase 1)
│   └── ingestion/
│       ├── models.py               # RedditPost, IngestionLog
│       ├── tasks.py                # Celery tasks (data collection)
│       ├── filters.py              # NoiseFilter class
│       ├── views.py                # API endpoints
│       ├── admin.py                # Django admin configuration
│       ├── urls.py                 # App URL routing
│       ├── apps.py                 # App configuration
│       ├── tests.py                # Unit tests
│       └── migrations/             # Database migrations
│
├── 🐳 Docker & Deployment
│   ├── Dockerfile                  # Container image definition
│   ├── docker-compose.yml          # Multi-service orchestration
│   ├── init.sh                     # Database initialization script
│   └── dev-setup.sh                # Local development setup
│
├── 📂 Application Directories
│   ├── templates/                  # HTML templates (future use)
│   ├── static/                     # CSS, JS, images
│   ├── media/                      # User uploads
│   ├── logs/                       # Application logs
│   └── .git/                       # Git version control
│
└── ⚙️ Configuration
    ├── .env.example                # Environment template (safe)
    ├── .env                        # Secrets (never commit!)
    └── .gitignore                  # Git ignore patterns
```

---

## 🎯 What Each File Does

### Configuration Files
- **`settlement_needs/settings.py`** - All Django settings (database, Celery, logging, etc.)
- **`.env`** - Environment variables (credentials, database, etc.)
- **`requirements.txt`** - Python packages to install

### Application Core
- **`ingestion/models.py`** - Database models (RedditPost, IngestionLog)
- **`ingestion/tasks.py`** - Background job logic (data collection)
- **`ingestion/filters.py`** - Spam/noise filtering implementation
- **`ingestion/views.py`** - REST API endpoints
- **`ingestion/admin.py`** - Django admin interface configuration

### Testing & Documentation
- **`ingestion/tests.py`** - Unit tests for models and filters
- **All `.md` files** - Documentation and guides

### Deployment & Setup
- **`Dockerfile`** - Container image specification
- **`docker-compose.yml`** - Multi-container orchestration
- **`dev-setup.sh`** - Automated local setup script
- **`manage.py`** - Django command-line interface

---

## 🚀 Quick Start Paths

### 🐳 Docker (Easiest - 2 minutes)
```bash
cp .env.example .env
# Edit .env with Reddit credentials
docker-compose up
# In another terminal:
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
# Visit http://localhost:8000/admin
```
→ See [SETUP_GUIDE.md](./SETUP_GUIDE.md#option-1-docker-recommended---easiest)

### 💻 Local Development (5 minutes)
```bash
./dev-setup.sh
# Follow instructions to start services
```
→ See [DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md#-getting-started-in-5-minutes)

### 📚 Full Setup with Details (15 minutes)
→ Follow [SETUP_GUIDE.md](./SETUP_GUIDE.md) step-by-step

---

## 📊 Technology Stack Quick Reference

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | Django | 5.1 | Web framework |
| **Language** | Python | 3.12 | Backend language |
| **Database** | PostgreSQL | 12+ | Data persistence |
| **Task Queue** | Celery | 5.3 | Background jobs |
| **Message Broker** | Redis | 6+ | Task messaging |
| **API Client** | PRAW | 7.7 | Reddit API access |
| **Server** | Gunicorn | 21.2 | Production WSGI |
| **Container** | Docker | Latest | Containerization |
| **Testing** | pytest | 7.4 | Test framework |

---

## 🔑 Key Concepts

### Data Flow
Reddit → PRAW API → Python Task → Filtering → Database → API → Admin/Dashboard

### Models
- **RedditPost** - Stores collected Reddit posts with filtering metadata
- **IngestionLog** - Tracks data collection job execution and results

### Main Task
- **`ingest_reddit_posts`** - Celery task that runs every hour, collects Reddit posts, filters them, and stores in database

### Noise Filters
Remove posts that are:
- Low quality (short title/content)
- Promotional (URLs, ads, sales pitches)
- Spam (crypto, gambling, "make money fast")
- Deleted content (author is "[deleted]")

### API Endpoints
- `GET /ingestion/status/` - System statistics
- `GET /ingestion/posts/` - List posts (paginated)
- `GET /ingestion/posts/<id>/` - Post details
- `GET /ingestion/logs/` - Ingestion job logs

---

## 🧪 Development Workflow

### First Time Setup
1. Clone repository
2. Copy `.env.example` to `.env`
3. Add Reddit API credentials to `.env`
4. Run `./dev-setup.sh` (local) OR `docker-compose up` (Docker)
5. Create superuser: `python manage.py createsuperuser`
6. Access admin at `http://localhost:8000/admin`

### Making Changes
1. Edit code (models, tasks, filters, etc.)
2. Run tests: `python manage.py test`
3. Check logs: `tail -f logs/settlement_needs.log`
4. Test API endpoints locally
5. Commit with meaningful message
6. Push to repository

### Running Tasks
- **Manually trigger ingestion**: `python manage.py shell` → `from ingestion.tasks import ingest_reddit_posts; ingest_reddit_posts.apply_async()`
- **View recent posts**: `python manage.py shell` → `from ingestion.models import RedditPost; RedditPost.objects.all()[:5]`
- **Check logs**: `python manage.py shell` → `from ingestion.models import IngestionLog; IngestionLog.objects.all()[:5]`

### Monitoring
- **Admin Interface**: http://localhost:8000/admin (posts, logs, filters)
- **Celery Flower** (optional): `celery -A settlement_needs flower` (port 5555)
- **Logs**: `tail -f logs/settlement_needs.log`

---

## 🐛 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Redis connection error | Start Redis: `redis-server` |
| PostgreSQL connection error | Check `.env` credentials, ensure PostgreSQL is running |
| Reddit API auth fails | Verify credentials at https://reddit.com/prefs/apps |
| No posts being collected | Check TARGET_KEYWORDS in tasks.py match actual posts |
| Celery tasks not running | Verify worker is running, check Redis, review logs |
| Admin page not loading | Run `python manage.py migrate` |
| Import errors | Run `pip install -r requirements.txt` |

See [SETUP_GUIDE.md](./SETUP_GUIDE.md#-troubleshooting) for detailed troubleshooting.

---

## 📈 Project Phases

### ✅ Phase 1: Data Ingestion (COMPLETE)
- Reddit data collection
- Noise filtering
- Database storage
- API endpoints
- Admin interface

### 🔄 Phase 2-6 (In Planning)
- **Phase 2**: ML classification
- **Phase 3**: Enhanced backend
- **Phase 4**: Alert system
- **Phase 5**: Analytics dashboard
- **Phase 6**: Model retraining & deployment

→ See [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md) for complete roadmap

---

## 🔒 Important Security Notes

⚠️ **NEVER:**
- Commit `.env` file
- Commit database passwords
- Commit Reddit API credentials
- Commit email passwords
- Use same credentials in dev and production

✅ **ALWAYS:**
- Use `.env.example` as template
- Use environment variables for secrets
- Keep dependencies updated
- Review git diff before committing
- Use strong, unique passwords

---

## 📞 Getting Help

### Questions about...
- **Project goals/roadmap** → [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)
- **Getting started** → [README.md](./README.md)
- **Setup/installation** → [SETUP_GUIDE.md](./SETUP_GUIDE.md)
- **Development** → [DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md)
- **Phase 1 details** → [PHASE_1_README.md](./PHASE_1_README.md)
- **Code** → See docstrings in files
- **API** → [SETUP_GUIDE.md](./SETUP_GUIDE.md#api-reference)

### External Resources
- [Django Documentation](https://docs.djangoproject.com/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [PRAW Documentation](https://praw.readthedocs.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)

---

## ✨ Next Steps

1. **Choose your path** - See "Quick Start Paths" above
2. **Follow setup guide** - [SETUP_GUIDE.md](./SETUP_GUIDE.md)
3. **Get familiar with code** - See [DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md)
4. **Run tests** - `python manage.py test`
5. **Access admin** - http://localhost:8000/admin
6. **Monitor ingestion** - Check logs and admin interface
7. **Contribute** - Make improvements and submit PRs

---

## 📊 File Statistics

- **Total Files**: 25+
- **Python Files**: 12
- **Documentation Files**: 5
- **Configuration Files**: 3
- **Docker Files**: 2
- **Shell Scripts**: 2

**Total Lines of Code**: ~5,000+ (setup + documentation)

---

## 📄 License

MIT License - Settlement Needs Project

**Created**: November 2024
**Status**: Phase 1 Complete ✅
**Next Phase**: ML Classification Engine

---

**🚀 Ready to get started? Go to [README.md](./README.md) or [SETUP_GUIDE.md](./SETUP_GUIDE.md)!**
