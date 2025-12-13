# Contributing to Neural Motion Lab

Thank you for your interest in contributing to Neural Motion Lab! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/neural-motion-lab.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

## Code Standards

### Style Guide

We follow PEP 8 style guidelines. Please ensure your code adheres to these standards:

- Use 4 spaces for indentation
- Maximum line length: 127 characters
- Use meaningful variable and function names
- Add docstrings to all public functions and classes

### Code Formatting

We use Black for code formatting:

```bash
black src/ tests/
```

### Linting

Run linters before submitting:

```bash
flake8 src/ tests/
mypy src/
```

### Type Hints

Please add type hints to all function signatures:

```python
def process_image(image: np.ndarray, size: tuple) -> np.ndarray:
    """Process an image."""
    pass
```

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run unit tests only
pytest tests/unit/

# Run with coverage
pytest tests/ --cov=neural_motion_lab --cov-report=html
```

### Writing Tests

- Write tests for all new features
- Maintain test coverage above 80%
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern

Example:

```python
def test_video_generation():
    # Arrange
    pipeline = VideoPipeline("models/hunyuan")
    image = np.zeros((512, 512, 3))
    
    # Act
    video = pipeline.generate_video(image, "test prompt")
    
    # Assert
    assert video.shape[0] == 16
```

## Documentation

### Docstrings

Use Google-style docstrings:

```python
def generate_video(image: np.ndarray, prompt: str, num_frames: int = 16) -> np.ndarray:
    """
    Generate a video from an input image.
    
    Args:
        image: Input image array
        prompt: Text prompt for generation
        num_frames: Number of frames to generate
        
    Returns:
        Generated video as numpy array
        
    Raises:
        ValueError: If image dimensions are invalid
    """
    pass
```

### Documentation Files

- Update documentation when adding new features
- Include code examples
- Keep documentation concise and clear

## Pull Request Process

1. **Update Documentation**: Ensure all documentation is updated
2. **Add Tests**: Include tests for new features
3. **Run Tests**: Ensure all tests pass
4. **Update CHANGELOG**: Add entry describing your changes
5. **Code Review**: Address all review comments
6. **Squash Commits**: Clean up commit history before merging

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] CHANGELOG updated
```

## Reporting Bugs

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run '...'
2. See error

**Expected behavior**
What you expected to happen.

**Environment:**
- OS: [e.g., Ubuntu 20.04]
- Python version: [e.g., 3.10]
- CUDA version: [e.g., 11.8]
- GPU: [e.g., RTX 3090]

**Additional context**
Any other context about the problem.
```

## Feature Requests

We welcome feature requests! Please:

1. Check if the feature already exists
2. Describe the use case
3. Explain why it would be useful
4. Provide examples if possible

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism
- Focus on what is best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

## Questions?

If you have questions, please:

1. Check the documentation
2. Search existing issues
3. Open a new issue with the "question" label

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Acknowledgments

Thank you to all contributors who help make Neural Motion Lab better!
