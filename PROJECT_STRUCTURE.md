# Sonify Project Structure

This document provides an overview of the Sonify project structure and explains the purpose of each file and directory.

## 📁 Root Directory

```
Sonify/
├── 📄 README.md                 # Project documentation and setup guide
├── 📄 LICENSE                   # MIT License
├── 📄 requirements.txt          # Python dependencies
├── 📄 .gitignore               # Git ignore rules
├── 📄 env.example              # Environment variables template
├── 📄 app.py                   # Main Flask application
├── 📄 config.py                # Configuration management
├── 📄 utils.py                 # Utility functions and helpers
├── 📄 run.py                   # Application entry point
├── 📄 quickstart.py            # Quick setup script
├── 📄 setup.py                 # Package setup for distribution
├── 📄 pyproject.toml           # Modern Python packaging config
├── 📄 Makefile                 # Development tasks and commands
├── 📄 Dockerfile               # Docker container configuration
├── 📄 docker-compose.yml       # Docker Compose for development
├── 📄 .dockerignore            # Docker ignore rules
├── 📄 CONTRIBUTING.md          # Contribution guidelines
├── 📄 CHANGELOG.md             # Version history and changes
└── 📄 PROJECT_STRUCTURE.md     # This file
```

## 🎨 Frontend (Templates & Static)

### Templates Directory (`templates/`)
```
templates/
├── 📄 base.html                # Base template with navigation and styling
├── 📄 index.html               # Landing page with features overview
├── 📄 dashboard.html           # User dashboard with music data
└── 📄 visualizations.html      # Interactive charts and graphs
```

### Static Directory (`static/`)
```
static/
├── 📁 css/
│   └── 📄 style.css            # Additional custom styles
├── 📁 js/
│   └── 📄 app.js               # JavaScript utilities and interactions
└── 📁 exports/
    └── 📄 .gitkeep             # Placeholder for exported files
```

## 🧪 Testing

### Tests Directory (`tests/`)
```
tests/
├── 📄 __init__.py              # Makes tests a Python package
└── 📄 test_app.py              # Unit tests for the application
```

## 🔧 Configuration & Development

### Configuration Files
- **`config.py`**: Flask configuration classes for different environments
- **`env.example`**: Template for environment variables
- **`pyproject.toml`**: Modern Python packaging and tool configuration
- **`setup.py`**: Traditional Python package setup

### Development Tools
- **`Makefile`**: Common development tasks (install, run, test, etc.)
- **`Dockerfile`**: Container configuration for deployment
- **`docker-compose.yml`**: Multi-service development environment
- **`.dockerignore`**: Files to exclude from Docker builds

## 🚀 Application Files

### Core Application
- **`app.py`**: Main Flask application with routes and Spotify integration
- **`utils.py`**: Utility functions for data processing and visualization
- **`run.py`**: Application entry point with startup checks
- **`quickstart.py`**: Automated setup script for new users

### Session & Data Storage
- **`flask_session/`**: Directory for Flask session files
- **`static/exports/`**: Directory for exported visualizations

## 📚 Documentation

### User Documentation
- **`README.md`**: Main project documentation and setup guide
- **`PROJECT_STRUCTURE.md`**: This file - project structure overview

### Developer Documentation
- **`CONTRIBUTING.md`**: Guidelines for contributors
- **`CHANGELOG.md`**: Version history and release notes

## 🔐 Security & Environment

### Environment Management
- **`env.example`**: Template showing required environment variables
- **`.env`**: User's local environment file (not in git)
- **`.gitignore`**: Excludes sensitive files from version control

### Security Features
- OAuth 2.0 authentication with Spotify
- Session management
- Environment variable configuration
- Input validation and sanitization

## 🎯 Key Features by File

### Authentication & API (`app.py`)
- Spotify OAuth integration
- User session management
- API endpoints for data retrieval
- Route protection and error handling

### Data Visualization (`utils.py`)
- Chart generation with Plotly
- Data processing and analysis
- Export functionality
- Audio feature analysis

### User Interface (`templates/`)
- Responsive Bootstrap 5 design
- Interactive charts and graphs
- Mobile-friendly layout
- Dark mode support

### Development Tools (`Makefile`)
- Automated setup and installation
- Testing and linting commands
- Code formatting
- Docker deployment

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Browser  │    │   Flask App     │    │  Spotify API    │
│                 │    │                 │    │                 │
│  - HTML/CSS/JS  │◄──►│  - Routes       │◄──►│  - User Data    │
│  - Charts       │    │  - Auth         │    │  - Music Info   │
│  - Export       │    │  - Processing   │    │  - Audio Feat.  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Data Storage  │
                       │                 │
                       │  - Sessions     │
                       │  - Exports      │
                       │  - Cache        │
                       └─────────────────┘
```

## 🔄 Data Flow

1. **Authentication**: User logs in via Spotify OAuth
2. **Data Retrieval**: App fetches user's music data from Spotify API
3. **Processing**: Data is processed and analyzed using utility functions
4. **Visualization**: Charts and graphs are generated with Plotly
5. **Display**: Interactive visualizations are shown to the user
6. **Export**: Users can export charts as images

## 🛠️ Development Workflow

1. **Setup**: Run `python quickstart.py` or `make setup`
2. **Development**: Use `make run` to start development server
3. **Testing**: Use `make test` to run tests
4. **Linting**: Use `make lint` to check code style
5. **Formatting**: Use `make format` to format code
6. **Deployment**: Use Docker or traditional deployment methods

## 📦 Deployment Options

### Local Development
- Python virtual environment
- Flask development server
- Local file storage

### Docker Deployment
- Containerized application
- Environment variable configuration
- Health checks and monitoring

### Production Deployment
- WSGI server (Gunicorn)
- Reverse proxy (Nginx)
- SSL/TLS certificates
- Database for session storage

## 🔍 File Naming Conventions

- **Python files**: lowercase with underscores (`app.py`, `utils.py`)
- **HTML templates**: lowercase with underscores (`base.html`, `dashboard.html`)
- **CSS/JS files**: lowercase with underscores (`style.css`, `app.js`)
- **Configuration files**: lowercase with dots (`config.py`, `env.example`)
- **Documentation**: UPPERCASE with underscores (`README.md`, `CONTRIBUTING.md`)

## 📝 Code Organization

- **Separation of Concerns**: Each file has a specific purpose
- **Modular Design**: Functions and classes are organized logically
- **Configuration Management**: Environment-specific settings
- **Error Handling**: Comprehensive error handling throughout
- **Documentation**: Inline comments and docstrings
- **Testing**: Unit tests for core functionality

This structure provides a clean, maintainable, and scalable foundation for the Sonify Spotify data visualizer application. 