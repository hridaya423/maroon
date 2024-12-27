import re
from typing import Optional, Any
from .types import PirateType
from .exceptions import PirateException

class PatternHandler:
    def __init__(self, interpreter):
        self.interpreter = interpreter
        
    def handle_pattern(self, command: str) -> Optional[str]:
        list_comp = re.match(r'^(\w+)\s+be\s+list\s+of\s+(.+?)\s+where\s+each\s+(.+)$', command)
        if list_comp:
            return self._handle_list_comprehension(
                list_comp.group(1), 
                list_comp.group(2),
                list_comp.group(3)
            )
            
        filter_match = re.match(r'^(\w+)\s+be\s+(.+?)\s+where\s+(.+)$', command)
        if filter_match:
            return self._handle_filter(
                filter_match.group(1),
                filter_match.group(2),
                filter_match.group(3)
            )

        reduce_match = re.match(r'^(\w+)\s+be\s+reduce\s+(.+?)\s+with\s+(.+)$', command)
        if reduce_match:
            return self._handle_reduce(
                reduce_match.group(1),
                reduce_match.group(2),
                reduce_match.group(3)
            )

        string_op = re.match(r'^(\w+)\s+be\s+(.+?)\s+(join|split|upper|lower|trim)\s*(.*)$', command)
        if string_op:
            return self._handle_string_operation(
                string_op.group(1),
                string_op.group(2),
                string_op.group(3),
                string_op.group(4)
            )
            
        return command

    def _handle_list_comprehension(self, var_name: str, items: str, operation: str) -> None:
        temp_list = [self.interpreter.parse_expression(item.strip()).value 
                    for item in items.split(',')]
        result_list = []
        
        for item in temp_list:
            curr_value = item
            ops = operation.replace("be ", "").split(" plus ")
            
            for op in ops:
                op_parts = op.split()
                if op_parts[0] == "times":
                    curr_value = curr_value * float(op_parts[1])
                    curr_value = float(curr_value)
            if "plus" in operation:
                curr_value = curr_value + float(ops[-1].split()[-1])
                
            result_list.append(curr_value)
        
        self.interpreter.treasure_chest[var_name] = PirateType(result_list, 'list')
        return None

    def _handle_filter(self, var_name: str, source: str, condition: str) -> None:
        source_list = self.interpreter.parse_expression(source)
        if not isinstance(source_list.value, list):
            raise PirateException("Can only filter lists")
            
        result = []
        for item in source_list.value:
            cond_parts = condition.replace("it be ", "").split()
            if len(cond_parts) == 2:
                op = cond_parts[0]
                threshold = float(cond_parts[1])
                
                if op == "greater_than" and item > threshold:
                    result.append(item)
                    
        self.interpreter.treasure_chest[var_name] = PirateType(result, 'list')
        return None

    def _handle_reduce(self, var_name: str, source: str, operation: str) -> None:
        source_val = self.interpreter.parse_expression(source)
        if not isinstance(source_val.value, list) or not source_val.value:
            raise PirateException("Cannot reduce empty or non-list")
            
        result = source_val.value[0]
        for item in source_val.value[1:]:
            if isinstance(result, PirateType):
                result = result.value
            result += item
                
        self.interpreter.treasure_chest[var_name] = PirateType(result)
        return None

    def _handle_string_operation(self, var_name: str, source: str, operation: str, args: str) -> None:
        source_val = self.interpreter.parse_expression(source)
        if not isinstance(source_val.value, (str, list)):
            raise PirateException("String operations require string or list input")
            
        result = None
        if operation == 'join':
            separator = args.strip('"') if args else ''
            if isinstance(source_val.value, list):
                result = separator.join(str(x) for x in source_val.value)
            else:
                raise PirateException("Join requires list input")
        elif operation == 'split':
            if isinstance(source_val.value, str):
                separator = args.strip('"') if args else None
                result = source_val.value.split(separator)
            else:
                raise PirateException("Split requires string input")
        elif operation in ['upper', 'lower', 'trim']:
            if isinstance(source_val.value, str):
                if operation == 'upper':
                    result = source_val.value.upper()
                elif operation == 'lower':
                    result = source_val.value.lower()
                else:
                    result = source_val.value.strip()
            else:
                raise PirateException(f"{operation} requires string input")
                
        self.interpreter.treasure_chest[var_name] = PirateType(result, 
            'list' if isinstance(result, list) else 'string')
        return None