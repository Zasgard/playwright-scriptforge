# Changelog

All notable changes to Playwright ScriptForge will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-12

### Added

- Initial release of Playwright ScriptForge
- Core conversion functionality:
  - Python to YAML converter with AST parsing
  - YAML to Python compiler with parameter substitution
- CLI interface with commands:
  - `record` - Record Playwright sessions using codegen
  - `convert` - Convert Python to YAML
  - `compile` - Compile YAML to Python
  - `validate` - Validate YAML scripts
- Docker support:
  - Dockerfile with Playwright browsers pre-installed
  - docker-compose.yml for easy container orchestration
  - Helper scripts (run.sh, quickstart.sh)
- Supported Playwright actions (12+):
  - navigate, click, fill, type, press
  - select, check, uncheck, hover
  - wait, wait_timeout, screenshot
- Parameter system:
  - Automatic parameterization of URLs and form inputs
  - Command-line parameter overrides
  - ${parameter} syntax in YAML
- Documentation:
  - Comprehensive README.md
  - Detailed USAGE.md with examples
  - CONTRIBUTING.md for developers
  - ROADMAP.md for future plans
  - Example YAML scripts
- Development tools:
  - Makefile for common tasks
  - Test suite (test_scriptforge.py)
  - GitHub Actions workflow
  - .env.example for configuration
- MIT License

### Technical Details

- Python 3.8+ compatibility
- Playwright 1.48.0
- Click CLI framework
- PyYAML for YAML processing
- AST-based Python code parsing
- Docker multi-stage build optimization

## [Unreleased]

### Planned

- File upload support
- Drag and drop actions
- Frame/iframe handling
- Assertion support
- Web UI for YAML editing
- Enhanced selector strategies
- pytest integration
- Performance metrics

---

[1.0.0]: https://github.com/Zasgard/playwright-scriptforge/releases/tag/v1.0.0
[Unreleased]: https://github.com/Zasgard/playwright-scriptforge/compare/v1.0.0...HEAD
