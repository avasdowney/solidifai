# Contributing to solidifai

Thank you for your interest in contributing to solidifai! This document provides guidelines and instructions for contributing.

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/avasdowney/solidifai.git
   cd solidifai
   ```

2. **Install in development mode:**
   ```bash
   pip install -e .
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

## Running Tests

Run the test suite using unittest:

```bash
python -m unittest discover tests/ -v
```

## Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose

## Adding New Features

1. **Create a new branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write clean, documented code
   - Add tests for new functionality
   - Update README if needed

3. **Test your changes:**
   ```bash
   python -m unittest discover tests/
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add: brief description of your changes"
   ```

5. **Push and create a pull request:**
   ```bash
   git push origin feature/your-feature-name
   ```

## Types of Contributions

### Bug Reports
- Use GitHub Issues
- Include clear description and steps to reproduce
- Include Python version and OS information

### Feature Requests
- Open a GitHub Issue with the "enhancement" label
- Describe the feature and its use case
- Discuss before implementing large changes

### Code Contributions
- Bug fixes
- New features
- Documentation improvements
- Test coverage improvements

## Project Structure

```
solidifai/
├── solidifai/           # Main package
│   ├── __init__.py     # Package initialization
│   ├── generator.py    # Core STL generation logic
│   └── cli.py          # Command-line interface
├── tests/              # Unit tests
│   ├── __init__.py
│   └── test_solidifai.py
├── demo.py             # Demo script
├── examples.py         # Example usage
├── requirements.txt    # Dependencies
├── setup.py           # Package setup
└── README.md          # Documentation
```

## Testing Guidelines

- Write tests for new features
- Ensure existing tests pass
- Use mocks for external API calls
- Test edge cases and error conditions

## Documentation

- Update README.md for user-facing changes
- Add docstrings to all public functions
- Include examples in docstrings
- Update CONTRIBUTING.md if development process changes

## Questions?

Feel free to open an issue for any questions or concerns.

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
