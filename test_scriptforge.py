"""
Basic tests for Playwright ScriptForge
Tests the Python to YAML and YAML to Python conversion
"""
import yaml
from python_to_yaml import python_to_yaml_dict
from yaml_to_python import compile_yaml_to_python


def test_python_to_yaml_conversion():
    """Test converting Playwright Python code to YAML"""
    python_code = '''
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")
    page.click("text=More information")
    page.fill("input[name='search']", "test query")
    page.screenshot(path="test.png")
    browser.close()
'''
    
    result = python_to_yaml_dict(python_code)
    
    assert 'actions' in result
    assert 'parameters' in result
    assert len(result['actions']) > 0
    
    # Check that actions were extracted
    action_types = [action['action'] for action in result['actions']]
    assert 'navigate' in action_types
    assert 'click' in action_types
    assert 'fill' in action_types
    
    print("✅ Python to YAML conversion test passed")


def test_yaml_to_python_compilation():
    """Test compiling YAML script to Python code"""
    yaml_dict = {
        'name': 'Test Script',
        'description': 'Test',
        'parameters': {
            'url': 'https://example.com',
            'search_term': 'playwright'
        },
        'actions': [
            {'action': 'navigate', 'url': '${url}'},
            {'action': 'fill', 'selector': 'input[name="q"]', 'value': '${search_term}'},
            {'action': 'click', 'selector': 'button[type="submit"]'},
        ]
    }
    
    python_code = compile_yaml_to_python(yaml_dict)
    
    # Check that Python code contains expected elements
    assert 'from playwright.sync_api import sync_playwright' in python_code
    assert 'def run(playwright):' in python_code
    assert 'page.goto("https://example.com")' in python_code
    assert 'page.fill("input[name=\\"q\\"]", "playwright")' in python_code
    assert 'page.click("button[type=\\"submit\\"]")' in python_code
    
    print("✅ YAML to Python compilation test passed")


def test_round_trip_conversion():
    """Test full round-trip: Python -> YAML -> Python"""
    original_python = '''
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto("https://test.com")
    page.fill("input#username", "testuser")
    page.click("button#submit")
    browser.close()
'''
    
    # Convert to YAML
    yaml_dict = python_to_yaml_dict(original_python)
    
    # Compile back to Python
    compiled_python = compile_yaml_to_python(yaml_dict)
    
    # Verify the compiled code has the expected structure
    assert 'def run(playwright):' in compiled_python
    assert 'page.goto(' in compiled_python
    assert 'page.fill(' in compiled_python
    assert 'page.click(' in compiled_python
    
    print("✅ Round-trip conversion test passed")


def test_parameter_substitution():
    """Test that parameters are correctly substituted"""
    yaml_dict = {
        'parameters': {
            'base_url': 'https://example.com',
            'username': 'admin',
            'password': 'secret'
        },
        'actions': [
            {'action': 'navigate', 'url': '${base_url}/login'},
            {'action': 'fill', 'selector': '#user', 'value': '${username}'},
            {'action': 'fill', 'selector': '#pass', 'value': '${password}'},
        ]
    }
    
    python_code = compile_yaml_to_python(yaml_dict)
    
    # Check that parameters were substituted
    assert 'https://example.com/login' in python_code
    assert '"admin"' in python_code
    assert '"secret"' in python_code
    
    print("✅ Parameter substitution test passed")


if __name__ == '__main__':
    print("Running Playwright ScriptForge tests...\n")
    
    test_python_to_yaml_conversion()
    test_yaml_to_python_compilation()
    test_round_trip_conversion()
    test_parameter_substitution()
    
    print("\n🎉 All tests passed!")
