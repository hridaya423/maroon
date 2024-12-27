from typing import Any, List, Optional
from .types import PirateType
from .exceptions import PirateException
import re

class LoopHandler:
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def handle_loop(self, command: str) -> Optional[Any]:
        try:
            while_match = self.parse_while_loop(command)
            if while_match:
                self.execute_while_loop(*while_match)
                return True
            plunder_match = self.parse_plunder_loop(command)
            if plunder_match:
                self.execute_plunder_loop(*plunder_match)
                return True
            repeat_match = self.parse_repeat_loop(command)
            if repeat_match:
                self.execute_repeat_loop(*repeat_match)
                return True

            return None
        except Exception as e:
            if isinstance(e, PirateException):
                raise e
            raise PirateException(str(e))

    def parse_while_loop(self, command: str) -> Optional[tuple]:
        basic_match = re.match(r'^while\s+(\w+)\s+be\s+(.+?)\s+(.+)$', command)
        if basic_match:
            var_name = basic_match.group(1)
            condition = basic_match.group(2)
            action = basic_match.group(3)
            return (var_name, condition, action, None, None)

        comp_match = re.match(r'^while\s+(\w+)\s+be\s+(less_than|greater_than|equals|greater_or_equal|less_or_equal)\s+(.+?)\s+(.+)$', command)
        if comp_match:
            var_name = comp_match.group(1)
            comparison = comp_match.group(2)
            target = comp_match.group(3)
            action = comp_match.group(4)
            return (var_name, None, action, comparison, target)
            
        return None

    def parse_plunder_loop(self, command: str) -> Optional[tuple]:
        match = re.match(r'^plunder\s+each\s+(\w+)\s+from\s+(\w+)\s+(.+)$', command)
        if match:
            var_name = match.group(1)
            list_name = match.group(2)
            action = match.group(3)
            return (var_name, list_name, action)
        return None

    def parse_repeat_loop(self, command: str) -> Optional[tuple]:
        match = re.match(r'^repeat\s+(.+?)\s+times\s+(.+)$', command)
        if match:
            count = match.group(1)
            action = match.group(2)
            return (count, action)
        return None

    def execute_plunder_loop(self, var_name: str, list_name: str, action: str) -> None:
        try:
            lst = self.interpreter.resolve_variable(list_name)
            if not isinstance(lst, PirateType) or not isinstance(lst.value, list):
                raise PirateException(f"Blimey! {list_name} ain't a chest of treasure!")

            self.interpreter.push_scope()
            for item in lst.value:
                self.interpreter.treasure_chest[var_name] = PirateType(item)
                self.interpreter.parse_command(action)
            self.interpreter.pop_scope()
            
        except Exception as e:
            if isinstance(e, PirateException):
                raise e
            raise PirateException(f"Failed to plunder the booty: {str(e)}")

    def execute_while_loop(self, var_name: str, condition: str, action: str, comparison: str = None, target: str = None) -> None:
        MAX_ITERATIONS = 10000
        iterations = 0
        
        try:
            while iterations < MAX_ITERATIONS:
                var_value = self.interpreter.resolve_variable(var_name)
                current_val = var_value.value if isinstance(var_value, PirateType) else var_value
              
                if comparison and target:
                    target_val = self.interpreter.parse_expression(target)
                    target_val = target_val.value if isinstance(target_val, PirateType) else target_val
                    if not self.interpreter.pirate_ops[comparison](current_val, target_val):
                        break
                elif str(current_val) != condition:
                    break
                action_result = self.interpreter.parse_command(action)
                
                if comparison and isinstance(current_val, (int, float)):
                    updated_value = current_val
                    if 'counter' in action or var_name in action:
                        continue
                    if comparison in ['less_than', 'less_or_equal']:
                        updated_value = current_val + 1
                    elif comparison in ['greater_than', 'greater_or_equal']:
                        updated_value = current_val - 1
                    self.interpreter.treasure_chest[var_name] = PirateType(updated_value)
                
                iterations += 1
                if iterations >= MAX_ITERATIONS:
                    raise PirateException("Blimey! We're caught in a whirlpool! (Loop limit exceeded)")
                
        except Exception as e:
            if isinstance(e, PirateException):
                raise e
            raise PirateException(f"Lost our bearings: {str(e)}")

    def execute_repeat_loop(self, count: str, action: str) -> None:
        try:
            if count.isdigit():
                iterations = int(count)
            else:
                count_val = self.interpreter.resolve_variable(count)
                iterations = int(count_val.value if isinstance(count_val, PirateType) else count_val)
            
            if iterations < 0:
                raise PirateException("Can't go back in time, ye scurvy dog!")
            if iterations > 10000:
                raise PirateException("That's too many times, ye trying to sink us?!")
            
            for _ in range(iterations):
                self.interpreter.parse_command(action)
                
        except Exception as e:
            if isinstance(e, PirateException):
                raise e
            raise PirateException(f"Loop went overboard: {str(e)}")