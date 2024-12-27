from typing import List, Any, Dict
from .exceptions import PirateException
from .types import PirateType

class SwitchCaseHandler:
    def __init__(self, interpreter):
        self.interpreter = interpreter
        
    def handle_switch(self, command: str) -> bool:
        if command.startswith('choose '):
            self._process_switch_block(command)
            return True
        return False
    
    def _process_switch_block(self, command: str):
        value_expr = command[7:].strip().rstrip(':')
        try:
            switch_value = self.interpreter.parse_expression(value_expr)
            if isinstance(switch_value, PirateType):
                switch_value = switch_value.value

            self.interpreter.current_switch = {
                'value': switch_value,
                'cases': [],
                'default': None,
                'in_progress': True
            }
            
        except Exception as e:
            raise PirateException(f"Invalid switch value: {str(e)}")
    
    def handle_case(self, command: str) -> bool:
        if not command.startswith('case '):
            return False
            
        if not hasattr(self.interpreter, 'current_switch'):
            raise PirateException("case statement outside of switch block")

        parts = command[5:].split(':', 1)
        if len(parts) != 2:
            raise PirateException("Invalid case syntax")
            
        case_expr = parts[0].strip()
        action = parts[1].strip()
        
        try:
            case_value = self.interpreter.parse_expression(case_expr)
            if isinstance(case_value, PirateType):
                case_value = case_value.value
                
            self.interpreter.current_switch['cases'].append({
                'value': case_value,
                'action': action
            })
            return True
            
        except Exception as e:
            raise PirateException(f"Invalid case value: {str(e)}")
    
    def handle_default(self, command: str) -> bool:
        if not command.startswith('default:'):
            return False
            
        if not hasattr(self.interpreter, 'current_switch'):
            raise PirateException("default statement outside of switch block")
            
        action = command[8:].strip()
        self.interpreter.current_switch['default'] = action
        return True
    
    def handle_end_switch(self, command: str) -> bool:
        if command != 'end choose':
            return False
            
        if not hasattr(self.interpreter, 'current_switch'):
            raise PirateException("end choose without matching choose")
            
        switch_data = self.interpreter.current_switch
        switch_value = switch_data['value']
        for case in switch_data['cases']:
            if case['value'] == switch_value:
                result = self.interpreter.parse_command(case['action'])
                delattr(self.interpreter, 'current_switch')
                return True
        if switch_data['default'] is not None:
            result = self.interpreter.parse_command(switch_data['default'])
            delattr(self.interpreter, 'current_switch')
            return True
            
        delattr(self.interpreter, 'current_switch')
        return True