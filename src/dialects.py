from typing import Optional
import re

class PirateDialect:
    def __init__(self, name: str):
        self.name = name
        self.mappings = {}
        self.special_patterns = [
            (r'^(\w+)\s+(\w+)\((.*?)\):$', r'voyage \2(\3):'),
            (r'^end\s+(\w+)$', r'end voyage'),
        ]
    
    def translate_to_core(self, command: str) -> str:
        parts = command.split('#', 1)
        cmd = parts[0].strip()
        comment = f"#{parts[1]}" if len(parts) > 1 else ""
        
        if not cmd:
            return command

        for pattern, replacement in self.special_patterns:
            match = re.match(pattern, cmd)
            if match:
                if match.re.pattern.endswith(r'\):$'): 
                    if match.group(1) in self.mappings and self.mappings[match.group(1)] == 'voyage':
                        result = f"voyage {match.group(2)}({match.group(3)}):"
                        return f"{result}{' ' + comment if comment else ''}"
                elif match.re.pattern.startswith('^end'): 
                    if match.group(1) in self.mappings and self.mappings[match.group(1)] == 'voyage':
                        return f"end voyage{' ' + comment if comment else ''}"

        result = cmd
        for dialect_word, core_word in self.mappings.items():
            pattern = r'\b' + re.escape(dialect_word) + r'\b'
            result = re.sub(pattern, core_word, result)
        
        return f"{result}{' ' + comment if comment else ''}"

class DialectManager:
    def __init__(self):
        self.dialects = {}
        self.current_dialect = None
        self.parsing_dialect = False
        self.active_dialect = None
    
    def parse_dialect_command(self, command: str) -> Optional[str]:
        cmd = command.split('#')[0].strip()
        if not cmd:
            return command

        dialect_start = re.match(r'^dialect\s+(\w+):$', cmd)
        if dialect_start:
            self.parsing_dialect = True
            self.current_dialect = PirateDialect(dialect_start.group(1))
            return None

        if cmd == 'end dialect':
            if self.parsing_dialect and self.current_dialect:
                self.dialects[self.current_dialect.name] = self.current_dialect
                self.active_dialect = self.current_dialect
                self.parsing_dialect = False
            return None

        if self.parsing_dialect and self.current_dialect:
            mapping_match = re.match(r'^\s*"([^"]+)"\s+be\s+"([^"]+)"$', cmd)
            if mapping_match:
                dialect_word = mapping_match.group(1)
                core_word = mapping_match.group(2)
                self.current_dialect.mappings[dialect_word] = core_word
                return None
        
        if self.active_dialect:
            return self.active_dialect.translate_to_core(command)
            
        return command

    def get_active_dialect_name(self) -> Optional[str]:
        return self.active_dialect.name if self.active_dialect else None