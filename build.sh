#!/bin/bash
# Build script for Render

echo "🚀 Starting build process..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Run database migrations (if any)
echo "🗄️  Setting up database..."
python -c "from app.core.database import engine; from app.models.base import Base; Base.metadata.create_all(bind=engine)"

echo "✅ Build completed!"