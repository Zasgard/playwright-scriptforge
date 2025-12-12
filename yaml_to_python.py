"""
YAML to Python Compiler for Playwright Scripts
Compiles YAML scripts with parameters back into executable Python code
"""
import re
from typing import Dict, Any, List


class YamlToPythonCompiler:
    """Compiles YAML script to Playwright Python code"""
    
    def __init__(self, yaml_dict: Dict[str, Any], parameters: Dict[str, str] = None):
        self.yaml_dict = yaml_dict
        self.parameters = parameters or yaml_dict.get('parameters', {})
        self.actions = yaml_dict.get('actions', [])
        
    def compile(self) -> str:
        """
        Compile YAML to executable Playwright Python code
        
        Returns:
            Python code as string
        """
        lines = []
        
        # Add imports
        lines.append("from playwright.sync_api import sync_playwright")
        lines.append("")
        
        # Add main function
        lines.append("def run(playwright):")
        lines.append("    browser = playwright.chromium.launch(headless=True)")
        lines.append("    context = browser.new_context()")
        lines.append("    page = context.new_page()")
        lines.append("")
        
        # Generate action code
        for action in self.actions:
            action_code = self._generate_action_code(action)
            if action_code:
                lines.append(f"    {action_code}")
        
        # Add cleanup
        lines.append("")
        lines.append("    context.close()")
        lines.append("    browser.close()")
        lines.append("")
        
        # Add main execution
        lines.append("if __name__ == '__main__':")
        lines.append("    with sync_playwright() as playwright:")
        lines.append("        run(playwright)")
        
        return "\n".join(lines)
    
    def _generate_action_code(self, action: Dict[str, Any]) -> str:
        """Generate Python code for a single action"""
        action_type = action.get('action')
        
        if action_type == 'navigate':
            url = self._resolve_parameter(action.get('url', ''))
            return f'page.goto("{self._escape_string(url)}")'
        
        elif action_type == 'click':
            selector = self._escape_string(action.get('selector', ''))
            return f'page.click("{selector}")'
        
        elif action_type == 'fill':
            selector = self._escape_string(action.get('selector', ''))
            value = self._resolve_parameter(action.get('value', ''))
            return f'page.fill("{selector}", "{self._escape_string(value)}")'
        
        elif action_type == 'type':
            selector = self._escape_string(action.get('selector', ''))
            text = self._resolve_parameter(action.get('value', ''))
            return f'page.type("{selector}", "{self._escape_string(text)}")'
        
        elif action_type == 'press':
            selector = self._escape_string(action.get('selector', ''))
            key = self._escape_string(action.get('key', ''))
            return f'page.press("{selector}", "{key}")'
        
        elif action_type == 'select':
            selector = self._escape_string(action.get('selector', ''))
            value = self._escape_string(action.get('value', ''))
            return f'page.select_option("{selector}", "{value}")'
        
        elif action_type == 'check':
            selector = self._escape_string(action.get('selector', ''))
            return f'page.check("{selector}")'
        
        elif action_type == 'uncheck':
            selector = self._escape_string(action.get('selector', ''))
            return f'page.uncheck("{selector}")'
        
        elif action_type == 'hover':
            selector = self._escape_string(action.get('selector', ''))
            return f'page.hover("{selector}")'
        
        elif action_type == 'wait':
            selector = self._escape_string(action.get('selector', ''))
            return f'page.wait_for_selector("{selector}")'
        
        elif action_type == 'wait_timeout':
            timeout = action.get('timeout', 1000)
            return f'page.wait_for_timeout({timeout})'
        
        elif action_type == 'screenshot':
            path = self._escape_string(action.get('path', 'screenshot.png'))
            return f'page.screenshot(path="{path}")'
        
        return ''
    
    def _escape_string(self, value: str) -> str:
        """Escape quotes in strings for Python code"""
        if not isinstance(value, str):
            return str(value)
        # Escape backslashes first, then quotes
        return value.replace('\\', '\\\\').replace('"', '\\"')
    
    def _resolve_parameter(self, value: str) -> str:
        """
        Resolve parameter placeholders in values
        
        Args:
            value: String that may contain ${param_name} placeholders
            
        Returns:
            Resolved string with actual parameter values
        """
        if not isinstance(value, str):
            return str(value)
        
        # Find all ${param_name} patterns
        pattern = r'\$\{([^}]+)\}'
        matches = re.findall(pattern, value)
        
        result = value
        for param_name in matches:
            if param_name in self.parameters:
                param_value = self.parameters[param_name]
                result = result.replace(f'${{{param_name}}}', str(param_value))
        
        return result


def compile_yaml_to_python(yaml_dict: Dict[str, Any], parameters: Dict[str, str] = None) -> str:
    """
    Compile YAML script to Python code
    
    Args:
        yaml_dict: Parsed YAML script as dictionary
        parameters: Optional parameter overrides
        
    Returns:
        Python code as string
    """
    compiler = YamlToPythonCompiler(yaml_dict, parameters)
    return compiler.compile()
