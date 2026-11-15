# Settlement Needs - Project Summary

## 🎯 Project Vision

**Settlement Needs** is a Django web application designed to identify gaps in settlement services for newcomers to Canada. It automatically collects and analyzes Reddit posts from immigration and Canadian communities to understand what services newcomers need, which services are already well-supported, and where significant gaps exist.

### Target Outcome
Provide government agencies, service providers, and community organizations with data-driven insights about settlement service demand and identify unmet needs in real time.

---

## 📅 Implementation Roadmap

### Phase 1: Data Ingestion Pipeline ✅ **COMPLETE**
**Collect and filter Reddit posts from targeted communities**

**Deliverables:**
- ✅ Automated Reddit data collection via PRAW API
- ✅ Noise reduction filtering system
- ✅ Django models and database schema
- ✅ Celery + Redis background task scheduling
- ✅ REST API for data access
- ✅ Django admin interface
- ✅ Docker containerization
- ✅ Unit tests and documentation

**Key Features:**
- Collects posts from r/ImmigrationCanada, r/PersonalFinanceCanada, r/askTO
- Filters by relevant keywords (COPR, settlement, housing, employment, etc.)
- Removes promotional, spam, and low-quality content
- Scheduled hourly data collection (configurable)
- Real-time status and logging

---

### Phase 2: Machine Learning Classification Engine
**Categorize posts into service domains and gap identification**

**Planned Deliverables:**
- NLP text preprocessing and tokenization
- Training dataset creation and labeling
- SVM classification model for settlement needs categories
- Confidence scoring system
- Model evaluation and metrics
- Integration with ingestion pipeline
- Automated classification on new posts

**Categories to Identify:**
- **Existing Services**: Employment assistance, housing/banking, health, language training
- **Unmet Needs**: Public transit, childcare, winter clothing, community integration
- **Confidence Scoring**: Reliability of classification for each post

---

### Phase 3: Core Django Backend & Database
**Enhance backend infrastructure for classification results**

**Planned Deliverables:**
- Enhanced database schema for classification results
- Confidence score storage and indexing
- Service/gap category taxonomy
- Data aggregation views
- Query optimization for analytics
- Historical tracking of classification changes

---

### Phase 4: Internal Early Warning & Triage System
**Alert staff about urgent needs and misclassifications**

**Planned Deliverables:**
- Alert rule configuration system
- Email/Slack notification system
- Caseworker triage dashboard
- Priority scoring system
- Direct outreach capability
- Alert log and analytics

**Alert Types:**
- Acute distress indicators (homelessness, hunger, etc.)
- Persistent unmet needs (trending gaps)
- Low-confidence predictions requiring human review
- Spam/moderation flags

---

### Phase 5: Analytics & Policy Dashboard
**Visualize demand patterns and identify service gaps**

**Planned Deliverables:**
- Real-time analytics dashboard
- Visual charts (demand trends, gap analysis)
- Service utilization metrics
- Geographic insights (if applicable)
- Temporal analysis (trends over time)
- Export capabilities for reports
- Policy recommendations engine

**Insights:**
- Which services are over/under capacity
- Trending unmet needs
- Seasonal patterns in settlement challenges
- Demographic insights (if identifiable)

---

### Phase 6: Human Feedback Loop & Deployment
**Enable model improvement and production deployment**

**Planned Deliverables:**
- Caseworker feedback UI within Django admin
- Model retraining pipeline
- A/B testing framework
- Docker production deployment
- Kubernetes orchestration (optional)
- CI/CD pipeline
- Monitoring and alerting
- Scaling infrastructure

**Continuous Improvement:**
- Caseworkers correct misclassifications
- Automated retraining triggers
- Model performance tracking
- Version control for models

---

## 🏗️ Technical Architecture

### Tech Stack
- **Backend**: Django 5.1 (Python 3.12)
- **Database**: PostgreSQL
- **Task Queue**: Celery + Redis
- **Data Source**: Reddit API (PRAW)
- **Deployment**: Docker + Docker Compose
- **Testing**: pytest, Django TestCase
- **Monitoring**: Celery Flower, Django admin, custom logging

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Reddit Platform                           │
│              (r/ImmigrationCanada, etc.)                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  PRAW Reddit API                            │
│            (Data Collection Interface)                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Phase 1: Ingestion Pipeline                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Celery Tasks (ingest_reddit_posts)                   │   │
│  │  • Fetch posts from target subreddits               │   │
│  │  • Apply keyword filtering                          │   │
│  │  • Run noise filters                                │   │
│  │  • Store in database                                │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│         Phase 2: ML Classification (Future)                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ SVM Classifier                                        │   │
│  │  • Categorize into service domains                   │   │
│  │  • Identify gaps vs. existing services              │   │
│  │  • Generate confidence scores                        │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              PostgreSQL Database                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ • RedditPost (raw data + classification)            │   │
│  │ • IngestionLog (job tracking)                       │   │
│  │ • Alert (Phase 4)                                   │   │
│  │ • MLModel (Phase 6)                                 │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
    ┌─────────┐ ┌────────┐ ┌──────────┐
    │ Admin   │ │ REST   │ │ Dashboard│
    │Interface│ │ API    │ │(Phase 5) │
    └─────────┘ └────────┘ └──────────┘
```

### Data Flow

```
1. COLLECTION
   Reddit API → PRAW → Python Task

2. FILTERING
   Keyword Match → Noise Filter → Valid/Invalid

3. STORAGE
   Valid Posts → PostgreSQL → RedditPost Model

4. CLASSIFICATION (Phase 2)
   Text → NLP → SVM → Categories + Confidence

5. ALERTING (Phase 4)
   Alert Rules → Match Posts → Email/Slack Notifications

6. ANALYTICS (Phase 5)
   Aggregated Data → Visualizations → Dashboard

7. FEEDBACK (Phase 6)
   Caseworker Corrections → Retraining → Model Improvement
```

---

## 📊 Database Schema (Phase 1)

### RedditPost Table
Stores raw Reddit posts with filtering metadata.

```sql
CREATE TABLE ingestion_redditpost (
    id SERIAL PRIMARY KEY,
    post_id VARCHAR(100) UNIQUE NOT NULL,
    subreddit VARCHAR(100) NOT NULL,
    author VARCHAR(100),
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    url VARCHAR(255) UNIQUE NOT NULL,
    upvotes INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    posted_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP AUTO_NOW_ADD,
    updated_at TIMESTAMP AUTO_NOW,
    is_valid BOOLEAN DEFAULT TRUE,
    is_noise BOOLEAN DEFAULT FALSE,
    noise_reason VARCHAR(255),
    is_promotional BOOLEAN DEFAULT FALSE,
    is_duplicate BOOLEAN DEFAULT FALSE
);
```

### IngestionLog Table
Tracks data collection job execution.

```sql
CREATE TABLE ingestion_ingestionlog (
    id SERIAL PRIMARY KEY,
    task_id VARCHAR(100) UNIQUE NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    posts_collected INTEGER DEFAULT 0,
    posts_filtered INTEGER DEFAULT 0,
    posts_saved INTEGER DEFAULT 0,
    error_message TEXT
);
```

---

## 🚀 Running Phase 1

### Quick Start (Docker)
```bash
cp .env.example .env
# Edit .env with Reddit credentials

docker-compose up
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Visit http://localhost:8000/admin
```

### Local Development
```bash
./dev-setup.sh

# Terminal 1: Django
python manage.py runserver

# Terminal 2: Celery Worker
celery -A settlement_needs worker -l info

# Terminal 3: Celery Beat
celery -A settlement_needs beat -l info
```

### API Endpoints
- `GET /ingestion/status/` - System statistics
- `GET /ingestion/posts/` - List posts
- `GET /ingestion/posts/<id>/` - Post details
- `GET /ingestion/logs/` - Job history

---

## 📈 Expected Data Volume (Phase 1)

Based on target subreddits and keywords:
- **Collection Frequency**: Every 1 hour (configurable)
- **Posts per Collection**: ~50-150 (with filtering)
- **Daily Posts**: ~600-1200 (after filtering)
- **Monthly Posts**: ~18,000-36,000
- **Database Growth**: ~1-2 GB per year (raw data)

---

## 🔐 Security & Privacy

### Reddit Data
- Only publicly available data is collected
- Posts are stored for analysis only
- No personal information beyond username is collected
- Compliance with Reddit's Terms of Service

### Database Security
- Environment variables for all credentials
- No secrets in source code
- PostgreSQL connection encryption recommended
- Regular backups

### Application Security
- CSRF protection enabled
- SQL injection prevention via ORM
- Input validation on all endpoints
- Rate limiting recommended for production

---

## 📋 Testing Strategy (Phase 1)

### Unit Tests
- Model validation
- Filter logic (spam, promotional, noise)
- Duplicate detection
- Database queries

### Integration Tests
- Reddit API connectivity
- End-to-end data ingestion
- Database storage and retrieval
- API endpoint responses

### Performance Tests
- Task execution time
- Database query optimization
- Memory usage under load
- Celery worker efficiency

---

## 📚 Documentation Files

1. **[PHASE_1_README.md](./PHASE_1_README.md)** - Phase 1 detailed guide
2. **[SETUP_GUIDE.md](./SETUP_GUIDE.md)** - Comprehensive setup and API reference
3. **[PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)** - This file
4. **Code docstrings** - Inline documentation in models, tasks, views

---

## 🤝 Contributing

### Development Workflow
1. Create feature branch from main
2. Make changes with clear commits
3. Add tests for new functionality
4. Update documentation
5. Submit pull request for review

### Code Standards
- PEP 8 compliance (use `black` for formatting)
- Meaningful variable names
- Comments for complex logic
- Type hints where applicable

---

## 🎓 Learning Resources

### Django
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)

### Celery
- [Celery Documentation](https://docs.celeryproject.org/)
- [Celery + Django Tutorial](https://celery.io//)

### Reddit API (PRAW)
- [PRAW Documentation](https://praw.readthedocs.io/)
- [Reddit API Documentation](https://www.reddit.com/dev/api)

### Machine Learning (Phase 2 Reference)
- [scikit-learn SVM](https://scikit-learn.org/stable/modules/svm.html)
- [NLTK for NLP](https://www.nltk.org/)

---

## 📞 Support & Questions

- **Documentation**: See [SETUP_GUIDE.md](./SETUP_GUIDE.md)
- **Issues**: Create a GitHub issue with detailed description
- **Pull Requests**: Submit improvements or bug fixes
- **Discussions**: Use GitHub discussions for questions

---

## 📄 License

MIT License - Settlement Needs Project

---

**Project Status**: Phase 1 Complete ✅ | Phases 2-6 In Planning

**Last Updated**: November 2024

**Next Milestone**: Phase 2 ML Classification Engine
