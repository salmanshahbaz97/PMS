#!/bin/bash

# Player Management System - Deployment Script
echo "🚀 Starting deployment process..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Create superuser if needed
echo "👤 Creating superuser..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

echo "✅ Deployment completed successfully!"
echo "🌐 Your app should now be running!"
echo "🔗 Admin URL: http://localhost:8000/admin/"
echo "👤 Admin credentials: admin / admin123" 