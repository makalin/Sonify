# Contributing to Sonify

Thank you for your interest in contributing to Sonify! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A Spotify Developer account (for testing)

### Setup Development Environment

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/makalin/Sonify.git
   cd Sonify
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .[dev]  # Install development dependencies
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your Spotify API credentials
   ```

5. **Run the application**
   ```bash
   make run
   # or
   python run.py
   ```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_app.py

# Run with coverage
pytest --cov=app tests/
```

### Writing Tests
- Tests should be in the `tests/` directory
- Use descriptive test names
- Test both success and failure cases
- Mock external API calls

## 📝 Code Style

### Python Code
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Keep functions small and focused
- Add docstrings for public functions

### Formatting
```bash
# Format code with black
make format

# Check code style with flake8
make lint
```

### Pre-commit Hooks
Consider setting up pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

## 🔧 Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes
- Write clear, descriptive commit messages
- Keep commits focused and atomic
- Test your changes thoroughly

### 3. Commit Your Changes
```bash
git add .
git commit -m "feat: add new visualization feature"
```

### 4. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

## 📋 Pull Request Guidelines

### Before Submitting
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] No sensitive data is committed

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No console errors
```

## 🐛 Reporting Bugs

### Bug Report Template
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
A clear description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
- OS: [e.g. macOS, Windows, Linux]
- Python version: [e.g. 3.9.0]
- Browser: [e.g. Chrome, Firefox]

**Additional context**
Add any other context about the problem here.
```

## 💡 Feature Requests

### Feature Request Template
```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
A clear description of any alternative solutions.

**Additional context**
Add any other context or screenshots about the feature request.
```

## 📚 Documentation

### Code Documentation
- Use docstrings for all public functions and classes
- Follow Google or NumPy docstring format
- Include type hints

### User Documentation
- Update README.md for user-facing changes
- Add inline comments for complex logic
- Document API endpoints

## 🔒 Security

### Security Guidelines
- Never commit API keys or secrets
- Use environment variables for sensitive data
- Validate all user inputs
- Follow OWASP security guidelines

### Reporting Security Issues
If you discover a security vulnerability, please email us at security@sonify.app instead of creating a public issue.

## 🏷️ Version Control

### Commit Message Format
Use conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

### Branch Naming
- `feature/feature-name`: New features
- `bugfix/bug-description`: Bug fixes
- `hotfix/urgent-fix`: Critical fixes
- `docs/documentation-update`: Documentation updates

## 🤝 Community Guidelines

### Code of Conduct
- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow the project's code of conduct

### Communication
- Use GitHub issues for discussions
- Be clear and concise
- Ask questions when needed
- Share knowledge and resources

## 📞 Getting Help

### Resources
- [GitHub Issues](https://github.com/makalin/Sonify/issues)
- [GitHub Discussions](https://github.com/makalin/Sonify/discussions)
- [Documentation](https://github.com/makalin/Sonify#readme)

### Questions?
If you have questions about contributing, feel free to:
1. Open a GitHub issue
2. Start a discussion
3. Contact the maintainers

Thank you for contributing to Sonify! 🎶 