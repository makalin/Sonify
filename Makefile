# Sonify - Makefile for common development tasks

.PHONY: help install run test clean lint format setup

# Default target
help:
	@echo "🎶 Sonify - Spotify Data Visualizer"
	@echo ""
	@echo "Available commands:"
	@echo "  setup     - Initial setup (install dependencies, create directories)"
	@echo "  install   - Install Python dependencies"
	@echo "  run       - Run the development server"
	@echo "  test      - Run tests"
	@echo "  lint      - Run linting checks"
	@echo "  format    - Format code with black"
	@echo "  clean     - Clean up generated files"
	@echo "  dist      - Build distribution package"
	@echo ""

# Initial setup
setup: install
	@echo "📁 Creating necessary directories..."
	mkdir -p static/exports
	mkdir -p flask_session
	@echo "✅ Setup complete! Don't forget to:"
	@echo "   1. Copy env.example to .env"
	@echo "   2. Add your Spotify API credentials to .env"
	@echo "   3. Run 'make run' to start the server"

# Install dependencies
install:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed!"

# Run development server
run:
	@echo "🚀 Starting Sonify development server..."
	python run.py

# Run tests
test:
	@echo "🧪 Running tests..."
	python -m pytest tests/ -v

# Run linting
lint:
	@echo "🔍 Running linting checks..."
	flake8 app.py utils.py config.py run.py
	@echo "✅ Linting complete!"

# Format code
format:
	@echo "🎨 Formatting code..."
	black app.py utils.py config.py run.py
	@echo "✅ Code formatted!"

# Clean up generated files
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	@echo "✅ Cleanup complete!"

# Build distribution package
dist: clean
	@echo "📦 Building distribution package..."
	python setup.py sdist bdist_wheel
	@echo "✅ Distribution package built!"

# Install in development mode
dev-install:
	@echo "🔧 Installing in development mode..."
	pip install -e .
	@echo "✅ Development installation complete!"

# Check for security vulnerabilities
security:
	@echo "🔒 Checking for security vulnerabilities..."
	safety check
	@echo "✅ Security check complete!"

# Generate requirements with versions
freeze:
	@echo "📋 Generating requirements.txt with exact versions..."
	pip freeze > requirements.freeze.txt
	@echo "✅ Requirements frozen to requirements.freeze.txt"

# Database migrations (if needed in future)
migrate:
	@echo "🗄️ Running database migrations..."
	@echo "No migrations needed for current version"

# Production deployment preparation
prod-prep:
	@echo "🚀 Preparing for production deployment..."
	@echo "1. Set FLASK_ENV=production in .env"
	@echo "2. Set FLASK_DEBUG=False in .env"
	@echo "3. Update SPOTIPY_REDIRECT_URI to your production domain"
	@echo "4. Set a strong SECRET_KEY"
	@echo "5. Configure your web server (nginx, etc.)"
	@echo "6. Set up SSL certificates"
	@echo "✅ Production preparation guide displayed!"

# Docker commands (if needed in future)
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t sonify .

docker-run:
	@echo "🐳 Running Docker container..."
	docker run -p 5000:5000 --env-file .env sonify

# Help for environment setup
env-help:
	@echo "🔧 Environment Setup Help:"
	@echo ""
	@echo "1. Copy the example environment file:"
	@echo "   cp env.example .env"
	@echo ""
	@echo "2. Get Spotify API credentials:"
	@echo "   - Go to https://developer.spotify.com/dashboard"
	@echo "   - Create a new application"
	@echo "   - Add http://localhost:5000/callback to Redirect URIs"
	@echo "   - Copy Client ID and Client Secret to .env"
	@echo ""
	@echo "3. Update .env with your credentials:"
	@echo "   SPOTIPY_CLIENT_ID=your_client_id_here"
	@echo "   SPOTIPY_CLIENT_SECRET=your_client_secret_here"
	@echo ""
	@echo "4. Run the application:"
	@echo "   make run" 