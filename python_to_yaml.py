"""
Python to YAML Converter for Playwright Scripts
Parses Playwright codegen Python output and converts to YAML format with parameterization
"""
import ast
import re
from typing import Dict, List, Any, Optional


class PlaywrightPythonParser:
    """Parses Playwright Python code to extract actions"""
    
    def __init__(self, python_code: str):
        self.python_code = python_code
        self.actions = []
        
    def parse(self) -> List[Dict[str, Any]]:
        """Parse Python code and extract Playwright actions"""
        try:
            tree = ast.parse(self.python_code)
            self._extract_actions(tree)
            return self.actions
        except SyntaxError as e:
            raise ValueError(f"Invalid Python syntax: {e}")
    
    def _extract_actions(self, node):
        """Recursively extract Playwright actions from AST"""
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                self._process_call(child)
    
    def _process_call(self, call_node: ast.Call):
        """Process a function call node to extract Playwright actions"""
        if isinstance(call_node.func, ast.Attribute):
            method_name = call_node.func.attr
            
            # Map Playwright methods to actions
            action_map = {
                'goto': self._extract_goto,
                'click': self._extract_click,
                'fill': self._extract_fill,
                'press': self._extract_press,
                'type': self._extract_type,
                'select_option': self._extract_select_option,
                'check': self._extract_check,
                'uncheck': self._extract_uncheck,
                'hover': self._extract_hover,
                'wait_for_selector': self._extract_wait,
                'wait_for_timeout': self._extract_wait_timeout,
                'screenshot': self._extract_screenshot,
            }
            
            if method_name in action_map:
                action = action_map[method_name](call_node)
                if action:
                    self.actions.append(action)
    
    def _extract_goto(self, node: ast.Call) -> Optional[Dict]:
        """Extract goto/navigate action"""
        if node.args:
            url = self._get_string_value(node.args[0])
            if url:
                return {
                    'action': 'navigate',
                    'url': url,
                    'parameterized': self._is_parameterizable(url)
                }
        return None
    
    def _extract_click(self, node: ast.Call) -> Optional[Dict]:
        """Extract click action"""
        if node.args:
            selector = self._get_string_value(node.args[0])
            if selector:
                return {
                    'action': 'click',
                    'selector': selector
                }
        return None
    
    def _extract_fill(self, node: ast.Call) -> Optional[Dict]:
        """Extract fill/input action"""
        if len(node.args) >= 2:
            selector = self._get_string_value(node.args[0])
            value = self._get_string_value(node.args[1])
            if selector:
                return {
                    'action': 'fill',
                    'selector': selector,
                    'value': value or '',
                    'parameterized': True  # Text inputs are always parameterizable
                }
        return None
    
    def _extract_press(self, node: ast.Call) -> Optional[Dict]:
        """Extract keyboard press action"""
        if len(node.args) >= 2:
            selector = self._get_string_value(node.args[0])
            key = self._get_string_value(node.args[1])
            if selector and key:
                return {
                    'action': 'press',
                    'selector': selector,
                    'key': key
                }
        return None
    
    def _extract_type(self, node: ast.Call) -> Optional[Dict]:
        """Extract type action"""
        if len(node.args) >= 2:
            selector = self._get_string_value(node.args[0])
            text = self._get_string_value(node.args[1])
            if selector:
                return {
                    'action': 'type',
                    'selector': selector,
                    'text': text or '',
                    'parameterized': True
                }
        return None
    
    def _extract_select_option(self, node: ast.Call) -> Optional[Dict]:
        """Extract select option action"""
        if len(node.args) >= 2:
            selector = self._get_string_value(node.args[0])
            value = self._get_string_value(node.args[1])
            if selector:
                return {
                    'action': 'select',
                    'selector': selector,
                    'value': value or ''
                }
        return None
    
    def _extract_check(self, node: ast.Call) -> Optional[Dict]:
        """Extract checkbox check action"""
        if node.args:
            selector = self._get_string_value(node.args[0])
            if selector:
                return {
                    'action': 'check',
                    'selector': selector
                }
        return None
    
    def _extract_uncheck(self, node: ast.Call) -> Optional[Dict]:
        """Extract checkbox uncheck action"""
        if node.args:
            selector = self._get_string_value(node.args[0])
            if selector:
                return {
                    'action': 'uncheck',
                    'selector': selector
                }
        return None
    
    def _extract_hover(self, node: ast.Call) -> Optional[Dict]:
        """Extract hover action"""
        if node.args:
            selector = self._get_string_value(node.args[0])
            if selector:
                return {
                    'action': 'hover',
                    'selector': selector
                }
        return None
    
    def _extract_wait(self, node: ast.Call) -> Optional[Dict]:
        """Extract wait for selector action"""
        if node.args:
            selector = self._get_string_value(node.args[0])
            if selector:
                return {
                    'action': 'wait',
                    'selector': selector
                }
        return None
    
    def _extract_wait_timeout(self, node: ast.Call) -> Optional[Dict]:
        """Extract wait timeout action"""
        if node.args:
            if isinstance(node.args[0], ast.Constant):
                timeout = node.args[0].value
                return {
                    'action': 'wait_timeout',
                    'timeout': timeout
                }
        return None
    
    def _extract_screenshot(self, node: ast.Call) -> Optional[Dict]:
        """Extract screenshot action"""
        path = None
        for keyword in node.keywords:
            if keyword.arg == 'path':
                path = self._get_string_value(keyword.value)
        
        return {
            'action': 'screenshot',
            'path': path or 'screenshot.png'
        }
    
    def _get_string_value(self, node) -> Optional[str]:
        """Extract string value from AST node"""
        if isinstance(node, ast.Constant):
            return str(node.value)
        elif isinstance(node, ast.Str):  # Python 3.7 compatibility
            return node.s
        return None
    
    def _is_parameterizable(self, value: str) -> bool:
        """Check if a value should be parameterized"""
        # URLs and text values are typically parameterizable
        return bool(value and not value.startswith('#'))


def python_to_yaml_dict(python_code: str) -> Dict[str, Any]:
    """
    Convert Playwright Python code to YAML-compatible dictionary
    
    Args:
        python_code: Playwright Python script from codegen
        
    Returns:
        Dictionary that can be serialized to YAML
    """
    parser = PlaywrightPythonParser(python_code)
    actions = parser.parse()
    
    # Build parameters dictionary from actions
    parameters = {}
    processed_actions = []
    
    for idx, action in enumerate(actions):
        processed_action = {'action': action['action']}
        
        # Handle parameterization
        if action['action'] == 'navigate' and action.get('parameterized'):
            param_name = 'url'
            parameters[param_name] = action['url']
            processed_action['url'] = f'${{{param_name}}}'
        elif action['action'] == 'navigate':
            processed_action['url'] = action['url']
            
        elif action['action'] in ['fill', 'type']:
            selector = action['selector']
            value = action.get('value') or action.get('text', '')
            
            # Create parameter name from selector
            param_name = f"input_{idx}"
            if 'name' in selector or 'id' in selector:
                match = re.search(r'(name|id)="([^"]+)"', selector)
                if match:
                    param_name = match.group(2)
            
            processed_action['selector'] = selector
            parameters[param_name] = value
            processed_action['value'] = f'${{{param_name}}}'
            
        elif action['action'] == 'click':
            processed_action['selector'] = action['selector']
            
        elif action['action'] == 'press':
            processed_action['selector'] = action['selector']
            processed_action['key'] = action['key']
            
        elif action['action'] == 'select':
            processed_action['selector'] = action['selector']
            processed_action['value'] = action['value']
            
        elif action['action'] in ['check', 'uncheck', 'hover', 'wait']:
            processed_action['selector'] = action['selector']
            
        elif action['action'] == 'wait_timeout':
            processed_action['timeout'] = action['timeout']
            
        elif action['action'] == 'screenshot':
            processed_action['path'] = action['path']
        
        processed_actions.append(processed_action)
    
    return {
        'name': 'Playwright Script',
        'description': 'Auto-generated from Playwright codegen',
        'parameters': parameters,
        'actions': processed_actions
    }
