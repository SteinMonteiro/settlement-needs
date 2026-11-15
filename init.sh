#!/bin/bash
# Initialize the Django application

set -e

echo "Waiting for database to be ready..."
python manage.py dbshell < /dev/null

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser..."
python manage.py createsuperuser --noinput \
    --username admin \
    --email admin@settlementneeds.local || echo "Superuser already exists"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "✓ Initialization complete!"
echo ""
echo "Next steps:"
echo "1. If using Docker: docker-compose up"
echo "2. If local: python manage.py runserver"
echo "3. Admin: http://localhost:8000/admin"
echo "4. API: http://localhost:8000/ingestion/"
