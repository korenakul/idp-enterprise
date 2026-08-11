# Contributing to IDP-Enterprise

Thank you for your interest in contributing to IDP-Enterprise! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Accept constructive feedback gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report, please check if the issue has already been reported. When creating a bug report, include:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Environment details (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

- A clear, descriptive title
- A detailed description of the proposed enhancement
- Any relevant examples or mockups
- Benefits of the enhancement

### Pull Requests

1. Fork the repository
2. Create a branch for your feature or fix (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests locally (`pytest tests/`)
5. Ensure code quality (`flake8 src/ tests/`, `mypy src/`)
6. Commit your changes with clear messages
7. Push to your fork
8. Open a pull request

## Development Setup

### Prerequisites

- Python 3.8+
- Poetry 1.6+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/idp-enterprise.git
cd idp-enterprise

# Install dependencies
poetry install --with dev

# Run tests
pytest tests/ --cov=src
```

## Coding Standards

### Python Style

- Follow PEP 8 guidelines
- Max line length: 120 characters
- Use type hints for all functions
- Include docstrings for all public functions and classes

### Naming Conventions

- Classes: `CamelCase`
- Functions/Variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Files/Directories: `snake_case`

### Documentation

- All public functions must have docstrings
- Update README.md for new features
- Add comments for complex logic
- Document API changes

## Testing

- Write unit tests for all new functionality
- Ensure existing tests pass
- Maintain or improve code coverage
- Tests should be independent and repeatable

## Commit Messages

Use conventional commit format:

```
<type>(<scope>): <description>

[optional body]

Types:
  feat:     A new feature
  fix:      A bug fix
  docs:     Documentation only changes
  style:    Code style changes (formatting, etc.)
  refactor: Code restructuring without functionality change
  test:     Adding or modifying tests
  chore:    Maintenance tasks
```

Example:
```
feat(ocr): add Google Vision engine support
```

## License

By contributing to IDP-Enterprise, you agree that your contributions will be licensed under the MIT License.