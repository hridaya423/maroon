import re
class FirstMate:
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.declared_variables = set()
        self.in_function = False
        self.current_function_params = set()
        self.current_function_name = None

    def track_variable_declaration(self, code_line: str):
        var_match = re.match(r'^(\w+)\s+be\s+', code_line)
        if var_match:
            self.declared_variables.add(var_match.group(1))
            
        func_match = re.match(r'^voyage\s+(\w+)\((.*?)\):$', code_line)
        if func_match:
            self.in_function = True
            self.current_function_name = func_match.group(1)
            params = [p.strip() for p in func_match.group(2).split(',') if p.strip()]
            self.current_function_params = set(params)
            
        if code_line.strip() == 'end voyage':
            self.in_function = False
            self.current_function_params.clear()
            self.current_function_name = None

    def analyze_code(self, code_line: str) -> str:
        self.track_variable_declaration(code_line)
        code_line = code_line.strip()

        if not code_line or code_line.startswith('#'):
            return None

        if 'sails with' in code_line:
            func_pattern = r'^(\w+)\s+sails\s+with\s+([^,]+(?:\s*,\s*[^,]+)*)$'
            if not re.match(func_pattern, code_line):
                return None

        if any(op in code_line for op in ['plus', 'minus', 'times', 'divided_by']):
            op_pattern = r'^\w+\s+be\s+.+?\s+(plus|minus|times|divided_by)\s+.+$'
            if not re.match(op_pattern, code_line):
                return None

        var_usage = re.search(r'\b(\w+)\s+be\s+', code_line)
        if var_usage:
            var_name = var_usage.group(1)
            if (var_name not in self.declared_variables and 
                var_name not in self.current_function_params and 
                not re.match(r'^-?\d*\.?\d+$', var_name)):
                return f"Variable '{var_name}' not found in the treasure chest!"

        if code_line.startswith('if'):
            cond_pattern = r'^if\s+.+?\s+be\s+(less_than|greater_than|equals|greater_or_equal|less_or_equal)\s+.+?\s*,\s*then\s+.+?(?:\s+else\s+.+)?$'
            if not re.match(cond_pattern, code_line):
                return "Invalid conditional! Use: if x be less_than y, then action else action"

        return None

    def provide_guidance(self, code_line: str, error: Exception = None) -> str:
        if error:
            error_str = str(error)
            if "Unknown function" in error_str:
                return f"First Mate: Ye haven't declared the function yet! Use 'voyage' to create it first."
            if "No treasure found" in error_str:
                var_match = re.search(r"No treasure found for (\w+)", error_str)
                if var_match:
                    return f"First Mate: '{var_match.group(1)}' isn't in the treasure chest! Declare it first."
        
        analysis = self.analyze_code(code_line)
        if analysis:
            return f"First Mate: {analysis}"
        return None