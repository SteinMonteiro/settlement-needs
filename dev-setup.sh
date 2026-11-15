#!/bin/bash
# Local development startup script

set -e

echo "🚀 Settlement Needs - Phase 1 Development Setup"
echo "================================================"

# Check Python version
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate venv
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Check Redis
echo "🔍 Checking Redis..."
if ! redis-cli ping > /dev/null 2>&1; then
    echo "⚠️  Redis is not running. Start it with: redis-server"
else
    echo "✓ Redis is running"
fi

# Check PostgreSQL
echo "🔍 Checking PostgreSQL..."
if ! psql -l > /dev/null 2>&1; then
    echo "⚠️  PostgreSQL is not running or credentials missing"
    echo "   Configure DB_HOST, DB_USER, DB_PASSWORD in .env"
fi

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Edit .env with your credentials before running"
    exit 1
fi

# Create logs directory
mkdir -p logs

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput -q

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps - Start these in separate terminals:"
echo ""
echo "  Terminal 1 (Django):"
echo "    source venv/bin/activate"
echo "    python manage.py runserver"
echo ""
echo "  Terminal 2 (Celery Worker):"
echo "    source venv/bin/activate"
echo "    celery -A settlement_needs worker -l info"
echo ""
echo "  Terminal 3 (Celery Beat):"
echo "    source venv/bin/activate"
echo "    celery -A settlement_needs beat -l info"
echo ""
echo "📊 Access points:"
echo "  • Admin:       http://localhost:8000/admin"
echo "  • API Status:  http://localhost:8000/ingestion/status/"
echo "  • Posts:       http://localhost:8000/ingestion/posts/"
echo "  • Logs:        http://localhost:8000/ingestion/logs/"
