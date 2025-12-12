# Playwright ScriptForge Usage Guide

This guide provides detailed examples and use cases for Playwright ScriptForge.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Workflow Examples](#workflow-examples)
4. [Advanced Usage](#advanced-usage)
5. [Troubleshooting](#troubleshooting)

## Installation

### Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/Zasgard/playwright-scriptforge.git
cd playwright-scriptforge

# Build the Docker image
docker-compose build

# Verify installation
docker-compose run scriptforge --help
```

### Local Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install --with-deps chromium firefox webkit

# Run CLI
python scriptforge.py --help
```

## Quick Start

### 1. Record a Session

Record your browser interactions:

```bash
docker-compose run scriptforge record --url https://example.com --output scripts/example.py
```

### 2. Convert to YAML

Convert the recorded Python to editable YAML:

```bash
docker-compose run scriptforge convert scripts/example.py
```

This creates `scripts/example.yaml` with parameterized inputs.

### 3. Edit Parameters

Edit `scripts/example.yaml` to customize parameters:

```yaml
parameters:
  url: https://my-custom-url.com
  username: my-user
  password: my-password
```

### 4. Compile to Python

Generate executable Python code:

```bash
docker-compose run scriptforge compile scripts/example.yaml
```

### 5. Execute

Run the compiled script:

```bash
docker-compose run scriptforge python scripts/example.py
```

## Workflow Examples

### Example 1: Web Form Automation

**Scenario:** Fill out a contact form with different data

```bash
# 1. Record the form filling
docker-compose run scriptforge record --url https://example.com/contact --output scripts/contact_form.py

# 2. Convert to YAML
docker-compose run scriptforge convert scripts/contact_form.py

# 3. Edit scripts/contact_form.yaml to add parameters
```

```yaml
parameters:
  name: John Doe
  email: john@example.com
  message: Hello World
  
actions:
  - action: navigate
    url: https://example.com/contact
  - action: fill
    selector: 'input[name="name"]'
    value: ${name}
  - action: fill
    selector: 'input[name="email"]'
    value: ${email}
  - action: fill
    selector: 'textarea[name="message"]'
    value: ${message}
  - action: click
    selector: 'button[type="submit"]'
```

```bash
# 4. Run with different data
docker-compose run scriptforge compile scripts/contact_form.yaml \
  --param name="Jane Smith" \
  --param email="jane@example.com" \
  --param message="Different message" \
  --output scripts/contact_jane.py

docker-compose run scriptforge python scripts/contact_jane.py
```

### Example 2: Login Flow Testing

**Scenario:** Test login with multiple user accounts

```bash
# 1. Record login flow
docker-compose run scriptforge record --url https://app.example.com/login --output scripts/login.py

# 2. Convert to YAML
docker-compose run scriptforge convert scripts/login.py

# 3. Create multiple test scripts
docker-compose run scriptforge compile scripts/login.yaml \
  --param username=admin@test.com \
  --param password=admin123 \
  --output scripts/login_admin.py

docker-compose run scriptforge compile scripts/login.yaml \
  --param username=user@test.com \
  --param password=user123 \
  --output scripts/login_user.py

# 4. Run all tests
docker-compose run scriptforge python scripts/login_admin.py
docker-compose run scriptforge python scripts/login_user.py
```

### Example 3: E-commerce Product Search

**Scenario:** Search for different products and capture results

```yaml
# scripts/product_search.yaml
parameters:
  search_term: laptop
  min_price: 500
  max_price: 1500

actions:
  - action: navigate
    url: https://shop.example.com
  - action: fill
    selector: 'input[name="search"]'
    value: ${search_term}
  - action: click
    selector: 'button.search-btn'
  - action: wait_timeout
    timeout: 2000
  - action: screenshot
    path: output/search_${search_term}.png
```

```bash
# Search for different products
for product in "laptop" "phone" "tablet"; do
  docker-compose run scriptforge compile scripts/product_search.yaml \
    --param search_term=$product \
    --output scripts/search_$product.py
  
  docker-compose run scriptforge python scripts/search_$product.py
done
```

### Example 4: Data Extraction

**Scenario:** Navigate and extract data from multiple pages

```yaml
# scripts/data_extraction.yaml
parameters:
  page_url: https://example.com/page/1
  output_file: data.json

actions:
  - action: navigate
    url: ${page_url}
  - action: wait
    selector: '.content-loaded'
  - action: screenshot
    path: output/page_screenshot.png
```

```bash
# Extract data from multiple pages
for page in {1..5}; do
  docker-compose run scriptforge compile scripts/data_extraction.yaml \
    --param page_url=https://example.com/page/$page \
    --output scripts/extract_page_$page.py
  
  docker-compose run scriptforge python scripts/extract_page_$page.py
done
```

## Advanced Usage

### Using Different Browsers

```bash
# Record with Firefox
docker-compose run scriptforge record --url https://example.com --browser firefox --output scripts/firefox_test.py

# Record with WebKit
docker-compose run scriptforge record --url https://example.com --browser webkit --output scripts/webkit_test.py
```

### Headless Recording

```bash
# Record in headless mode (non-interactive)
docker-compose run scriptforge record --url https://example.com --headless --output scripts/headless_test.py
```

### Validation Before Execution

Always validate YAML scripts before compiling:

```bash
docker-compose run scriptforge validate scripts/my_script.yaml
```

### Custom Volume Mounts

Edit `docker-compose.yml` to add custom directories:

```yaml
services:
  scriptforge:
    volumes:
      - ./scripts:/app/scripts
      - ./output:/app/output
      - ./data:/app/data  # Custom data directory
```

### Batch Processing

Create a shell script for batch processing:

```bash
#!/bin/bash
# batch_test.sh

URLS=(
  "https://example.com"
  "https://test.com"
  "https://demo.com"
)

for url in "${URLS[@]}"; do
  name=$(echo $url | sed 's/https:\/\///' | sed 's/\.com//')
  docker-compose run scriptforge compile scripts/template.yaml \
    --param url=$url \
    --output scripts/test_$name.py
  
  docker-compose run scriptforge python scripts/test_$name.py
done
```

### Environment Variables

Pass environment variables through docker-compose:

```yaml
services:
  scriptforge:
    environment:
      - TEST_ENV=production
      - API_KEY=${API_KEY}
```

Use in YAML scripts:

```yaml
parameters:
  api_key: ${API_KEY}  # Will be replaced at compile time
```

## Troubleshooting

### Issue: Docker build fails

**Solution:**
```bash
# Clean Docker cache
docker-compose down
docker system prune -a
docker-compose build --no-cache
```

### Issue: Playwright browsers not found

**Solution:**
```bash
# Rebuild container with browsers
docker-compose build --no-cache
```

### Issue: Permission denied on scripts

**Solution:**
```bash
# Fix permissions
chmod -R 755 scripts/
chmod -R 755 output/
```

### Issue: YAML validation fails

**Solution:**
Check YAML syntax:
```bash
docker-compose run scriptforge validate scripts/my_script.yaml
```

Common issues:
- Missing `actions` field
- Invalid indentation
- Missing parameter definitions

### Issue: Conversion misses actions

**Solution:**
The converter looks for specific Playwright method calls. Ensure your Python code uses standard Playwright syntax:
- `page.goto(url)` for navigation
- `page.click(selector)` for clicks
- `page.fill(selector, value)` for inputs

### Issue: Parameter substitution not working

**Solution:**
Ensure parameters are defined in the YAML:
```yaml
parameters:
  my_param: value

actions:
  - action: fill
    value: ${my_param}  # Correct
    # NOT: $my_param or {my_param}
```

## Best Practices

1. **Organize Scripts:** Keep scripts in the `scripts/` directory and outputs in `output/`
2. **Version Control:** Commit YAML scripts but not compiled Python
3. **Parameterize Everything:** URLs, credentials, search terms should all be parameters
4. **Validate Early:** Always validate YAML before compiling
5. **Test Incrementally:** Test one action at a time when building complex scripts
6. **Use Descriptive Names:** Name parameters clearly (e.g., `login_username` not just `user`)
7. **Add Waits:** Use `wait_timeout` or `wait` actions for dynamic content
8. **Take Screenshots:** Add screenshot actions to verify script execution

## Additional Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [YAML Syntax Guide](https://yaml.org/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
