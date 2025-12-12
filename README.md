# Playwright ScriptForge

**Round-trip automation workflow for Playwright** - Record once, edit many times.

Playwright ScriptForge is a Docker-based Python tool that enables a powerful workflow for browser automation:

1. 🎬 **Record** - Capture browser interactions using Playwright codegen
2. 🔄 **Convert** - Transform Python code into editable YAML with parameterized inputs
3. ⚙️ **Compile** - Generate executable Python code from YAML scripts
4. ▶️ **Replay** - Run the automation with different parameters without touching code

## Features

- **Docker-based** - Pre-configured container with Playwright browsers installed
- **Non-interactive CLI** - Perfect for CI/CD pipelines and automated workflows
- **Parameterization** - Edit inputs (URLs, form data, credentials) in simple YAML
- **Record-once, edit-many** - No need to re-record for different input values
- **Full Playwright support** - Navigate, click, fill, type, select, check, hover, wait, screenshot

## Quick Start

### Using Docker (Recommended)

1. **Build the container:**
```bash
docker-compose build
```

2. **Record a session:**
```bash
docker-compose run scriptforge record --url https://example.com --output scripts/my_script.py
```

3. **Convert to YAML:**
```bash
docker-compose run scriptforge convert scripts/my_script.py
```

4. **Edit parameters** in `scripts/my_script.yaml`:
```yaml
parameters:
  url: https://different-site.com
  username: newuser
  password: newpass
```

5. **Compile back to Python:**
```bash
docker-compose run scriptforge compile scripts/my_script.yaml
```

6. **Run the compiled script:**
```bash
docker-compose run scriptforge python scripts/my_script.py
```

### Local Installation

```bash
pip install -r requirements.txt
playwright install --with-deps chromium firefox webkit
python scriptforge.py --help
```

## CLI Commands

### `record` - Record a Playwright session

```bash
scriptforge record --url <URL> [OPTIONS]
```

**Options:**
- `--url` (required) - Starting URL for recording
- `--output, -o` - Output Python file (default: script.py)
- `--browser` - Browser choice: chromium, firefox, webkit (default: chromium)
- `--headless/--headed` - Run in headless mode (default: headed)

**Example:**
```bash
scriptforge record --url https://example.com --output my_recording.py --browser chromium
```

### `convert` - Convert Python to YAML

```bash
scriptforge convert <PYTHON_FILE> [OPTIONS]
```

**Options:**
- `--output, -o` - Output YAML file (default: <input>.yaml)

**Example:**
```bash
scriptforge convert my_recording.py --output my_script.yaml
```

### `compile` - Compile YAML to Python

```bash
scriptforge compile <YAML_FILE> [OPTIONS]
```

**Options:**
- `--output, -o` - Output Python file (default: <input>.py)
- `--param, -p` - Override parameter (can be used multiple times)

**Example:**
```bash
scriptforge compile my_script.yaml --param url=https://new-site.com --param username=admin
```

### `validate` - Validate YAML script

```bash
scriptforge validate <YAML_FILE>
```

**Example:**
```bash
scriptforge validate my_script.yaml
```

## YAML Script Format

YAML scripts have a simple structure:

```yaml
name: My Automation Script
description: Description of what this script does
parameters:
  url: https://example.com
  username: testuser
  password: testpass
  search_term: playwright
actions:
  - action: navigate
    url: ${url}
  - action: fill
    selector: 'input[name="username"]'
    value: ${username}
  - action: fill
    selector: 'input[name="password"]'
    value: ${password}
  - action: click
    selector: 'button[type="submit"]'
  - action: wait_timeout
    timeout: 2000
  - action: screenshot
    path: output/result.png
```

### Supported Actions

| Action | Description | Parameters |
|--------|-------------|------------|
| `navigate` | Navigate to URL | `url` |
| `click` | Click element | `selector` |
| `fill` | Fill input field | `selector`, `value` |
| `type` | Type text | `selector`, `value` |
| `press` | Press keyboard key | `selector`, `key` |
| `select` | Select option | `selector`, `value` |
| `check` | Check checkbox | `selector` |
| `uncheck` | Uncheck checkbox | `selector` |
| `hover` | Hover over element | `selector` |
| `wait` | Wait for selector | `selector` |
| `wait_timeout` | Wait for milliseconds | `timeout` |
| `screenshot` | Take screenshot | `path` |

### Parameter Substitution

Use `${parameter_name}` syntax to reference parameters:

```yaml
parameters:
  api_url: https://api.example.com
  api_key: secret123

actions:
  - action: navigate
    url: ${api_url}/dashboard
  - action: fill
    selector: 'input[name="apikey"]'
    value: ${api_key}
```

## Docker Configuration

### Dockerfile

The provided Dockerfile includes:
- Python 3.11
- Playwright with Chromium, Firefox, and WebKit browsers
- All system dependencies for browser automation

### docker-compose.yml

Pre-configured with:
- Volume mounts for `scripts/` and `output/` directories
- Container naming and environment setup

### Custom Configuration

Edit `docker-compose.yml` to customize:
```yaml
services:
  scriptforge:
    volumes:
      - ./scripts:/app/scripts
      - ./output:/app/output
      - ./custom_data:/app/data  # Add custom volumes
    environment:
      - PLAYWRIGHT_BROWSERS_PATH=/ms-playwright  # Custom browser path
```

## Examples

See the `examples/` directory for:
- `example_codegen.py` - Sample Playwright codegen output
- `example_script.yaml` - Basic YAML script with parameters
- `login_flow.yaml` - Login automation example

## Use Cases

1. **Test Automation** - Record test scenarios once, run with different test data
2. **Web Scraping** - Parameterize target URLs and search queries
3. **Form Filling** - Automate repetitive form submissions with varying data
4. **CI/CD Integration** - Run headless browser tests in Docker containers
5. **Cross-environment Testing** - Same script, different URLs for dev/staging/prod

## Workflow Example

Complete workflow for testing a login form:

```bash
# 1. Record the login flow
docker-compose run scriptforge record --url https://myapp.com/login --output scripts/login.py

# 2. Convert to editable YAML
docker-compose run scriptforge convert scripts/login.py

# 3. Edit scripts/login.yaml to parameterize credentials
# (Change hardcoded values to ${username} and ${password})

# 4. Run with different credentials
docker-compose run scriptforge compile scripts/login.yaml \
  --param username=user1 --param password=pass1 \
  --output scripts/login_user1.py

docker-compose run scriptforge compile scripts/login.yaml \
  --param username=user2 --param password=pass2 \
  --output scripts/login_user2.py

# 5. Execute the tests
docker-compose run scriptforge python scripts/login_user1.py
docker-compose run scriptforge python scripts/login_user2.py
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│  Playwright Codegen (Browser Recording)            │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
         ┌───────────────┐
         │  Python Code  │
         └───────┬───────┘
                 │ convert
                 ▼
         ┌───────────────┐
         │  YAML Script  │ ◄── Edit Parameters
         └───────┬───────┘
                 │ compile
                 ▼
         ┌───────────────┐
         │  Python Code  │
         └───────┬───────┘
                 │
                 ▼
         ┌───────────────┐
         │  Execute in   │
         │   Playwright  │
         └───────────────┘
```

## Troubleshooting

### Playwright not found
```bash
docker-compose build --no-cache
```

### Permission errors with volumes
```bash
chmod -R 777 scripts/ output/
```

### Browser launch fails
Ensure you're running inside Docker container:
```bash
docker-compose run scriptforge validate examples/example_script.yaml
```

## Contributing

Contributions welcome! This tool supports the record-once, edit-many workflow for Playwright automation.

## License

MIT License - See LICENSE file for details

## Links

- [Playwright Documentation](https://playwright.dev/python/)
- [Docker Documentation](https://docs.docker.com/)
- [YAML Specification](https://yaml.org/)