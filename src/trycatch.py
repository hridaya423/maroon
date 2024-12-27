from typing import List, Any
from .exceptions import PirateException

class TryCatchHandler:
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.in_try_block = False
        self.current_try_commands: List[str] = []
        self.error_handler: str = None
        
    def handle_try_start(self, command: str) -> bool:
        if command.strip() == "brace for impact:":
            self.in_try_block = True
            self.current_try_commands = []
            return True
        return False
    
    def handle_catch(self, command: str) -> bool:
        if command.startswith("if capsized"):
            if not self.in_try_block:
                raise PirateException("Found 'if capsized' without 'brace for impact'")
            self.error_handler = command[len("if capsized,"):].strip()
            self.execute_try_block()
            return True
        return False
    
    def collect_try_command(self, command: str):
        if self.in_try_block:
            self.current_try_commands.append(command)
            return True
        return False
    
    def execute_try_block(self):
        self.in_try_block = False
        try:
            for cmd in self.current_try_commands:
                self.interpreter.parse_command(cmd)
        except Exception as e:
            if self.error_handler:
                self.interpreter.parse_command(self.error_handler)
        finally:
            self.current_try_commands = []
            self.error_handler = None