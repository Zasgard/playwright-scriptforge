# Contributing to Playwright ScriptForge

Thank you for your interest in contributing to Playwright ScriptForge!

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in the [Issues](https://github.com/Zasgard/playwright-scriptforge/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Environment details (OS, Python version, Docker version)

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add tests for new features
   - Update documentation as needed

4. **Test your changes**
   ```bash
   # Run tests
   python test_scriptforge.py
   
   # Test CLI commands
   python scriptforge.py validate examples/example_script.yaml
   python scriptforge.py compile examples/example_script.yaml
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear description of your changes
   - Reference any related issues

## Development Setup

### Local Development

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/playwright-scriptforge.git
cd playwright-scriptforge

# Install dependencies
pip install -r requirements.txt
playwright install --with-deps chromium

# Run tests
python test_scriptforge.py
```

### Docker Development

```bash
# Build the image
docker-compose build

# Run tests in container
docker-compose run scriptforge python test_scriptforge.py
```

## Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise

## Testing

- Add tests for new features in `test_scriptforge.py`
- Ensure all existing tests pass
- Test with different Python versions (3.8+)
- Test both Docker and local installations

## Documentation

- Update README.md for major features
- Add examples to USAGE.md
- Document new CLI commands
- Update YAML schema documentation

## Areas for Contribution

### High Priority

- [ ] Add support for more Playwright actions (drag-and-drop, file uploads, etc.)
- [ ] Improve error messages and validation
- [ ] Add CI/CD pipeline (GitHub Actions)
- [ ] Support for async Playwright API
- [ ] Better handling of dynamic selectors

### Medium Priority

- [ ] Web UI for editing YAML scripts
- [ ] Support for test assertions
- [ ] Integration with test frameworks (pytest, unittest)
- [ ] Export to other formats (JSON, XML)
- [ ] Recording history and versioning

### Low Priority

- [ ] Support for mobile emulation
- [ ] Video recording of test execution
- [ ] Performance metrics collection
- [ ] Cloud storage integration
- [ ] Multi-language support

## Questions?

Feel free to:
- Open an issue for discussion
- Reach out to maintainers
- Join our community discussions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
