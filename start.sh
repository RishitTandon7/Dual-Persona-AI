#!/bin/bash

# Start the Flask application with Gunicorn for production
echo "🚀 Starting AI Shopping Assistant on Render..."
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
