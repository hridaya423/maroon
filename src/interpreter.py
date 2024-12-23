"""Core interpreter for Maroon"""
import re
import math
import operator
from typing import Any, Dict, List

from .exceptions import PirateException
from .types import PirateType
from .functions import PirateFunction

class PirateInterpreter:
    def __init__(self):
        self.scope_stack = [{}]
        self.ship_logs = {
            'bark': self.pirate_print,
            'count_booty': len,
            'plunder': lambda x: max(x.value if isinstance(x, PirateType) else x),
            'abandon': lambda x: min(x.value if isinstance(x, PirateType) else x),
            'type_of': lambda x: type(x).__name__,
            'debug_chest': self.debug_treasure_chest,
            'sqrt': math.sqrt,
            'abs': abs,
            'round': round,
            'to_int': int,
            'to_float': float,
            'to_str': str,
        }
        self.pirate_crew = {}
        self.pirate_ops = {
            'plus': operator.add,
            'minus': operator.sub,
            'times': operator.mul,
            'divided_by': operator.truediv,
            'modulo': operator.mod,
            'power': operator.pow,
            'equals': operator.eq,
            'greater_than': operator.gt,
            'less_than': operator.lt,
            'greater_or_equal': operator.ge,
            'less_or_equal': operator.le,
            'and': lambda x, y: x and y,
            'or': lambda x, y: x or y,
            'not': lambda x: not x,
        }
    
    def parse_expression(self, expr: str) -> Any:
        expr = expr.strip()

        func_call = re.match(r'^(\w+)\s+sails\s+with\s+(.+)$', expr)
        if func_call:
            func_name = func_call.group(1)
            arg = self.parse_expression(func_call.group(2))
            
            if func_name in self.ship_logs:
                result = self.ship_logs[func_name](arg)
                return PirateType(result)
            
            if func_name in self.pirate_crew:
                return self.execute_function(func_name, [arg])
            
            raise PirateException(f"Unknown function: {func_name}")

        if expr.startswith('"') and expr.endswith('"'):
            return PirateType(expr[1:-1], 'string')
        

        if expr.replace('.','',1).isdigit():
            value = float(expr) if '.' in expr else int(expr)
            return PirateType(value, 'number')
        

        if expr.lower() in ['true', 'false']:
            return PirateType(expr.lower() == 'true', 'boolean')
        

        list_index = re.match(r'^(\w+)\[(\d+)\]$', expr)
        if list_index:
            list_name = list_index.group(1)
            index = int(list_index.group(2))
            lst = self.resolve_variable(list_name)
            if isinstance(lst, PirateType) and isinstance(lst.value, list):
                return PirateType(lst.value[index])
            raise PirateException(f"{list_name} is not a list")
        

        try:
            return self.resolve_variable(expr)
        except PirateException:
            raise PirateException(f"Cannot parse expression: {expr}")

    def execute_function(self, func_name: str, args: List[Any]) -> Any:
        if func_name in self.pirate_crew:
            self.push_scope()
            func = self.pirate_crew[func_name]

            for param, arg in zip(func.params, args):
                self.treasure_chest[param] = arg
            
            result = None
            for cmd in func.body:
                if cmd.strip().startswith('return'):
                    result = self.parse_expression(cmd.strip()[7:])
                    break
                result = self.parse_command(cmd)
            
            self.pop_scope()
            return result
            
        raise PirateException(f"Unknown function: {func_name}")
    
    def pirate_print(self, *args):
        printed_args = []
        for arg in args:
            if isinstance(arg, PirateType):
                printed_args.append(f"{arg.value}")
            elif isinstance(arg, str):
                try:
                    value = self.resolve_variable(arg)
                    if isinstance(value, PirateType):
                        printed_args.append(f"{value.value}")
                    else:
                        printed_args.append(str(value))
                except PirateException:
                    printed_args.append(arg)
            else:
                printed_args.append(str(arg))
        print(" ".join(str(arg) for arg in printed_args))

    def debug_treasure_chest(self):
        print("🏴‍☠️ Current Treasure Chest Contents:")
        for name, value in self.treasure_chest.items():
            print(f"{name}: {value}")

    def push_scope(self):
        self.scope_stack.append({})

    def pop_scope(self):
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()

    @property
    def treasure_chest(self):
        return self.scope_stack[-1]

    def resolve_variable(self, var_name: str) -> Any:
        for scope in reversed(self.scope_stack):
            if var_name in scope:
                return scope[var_name]
        raise PirateException(f"No treasure found for {var_name}")

    def parse_command(self, command: str, line_number: int = None) -> Any:
        try:
            command = command.strip()
            
            if not command or command.startswith('#'):
                return None

            func_match = re.match(r'^voyage\s+(\w+)\((.*?)\):$', command)
            if func_match:
                func_name = func_match.group(1)
                params = [p.strip() for p in func_match.group(2).split(',') if p.strip()]
                self.current_function = PirateFunction(func_name, params, [])
                return None

            if command == 'end voyage':
                if hasattr(self, 'current_function'):
                    self.pirate_crew[self.current_function.name] = self.current_function
                    delattr(self, 'current_function')
                return None

            if hasattr(self, 'current_function'):
                self.current_function.body.append(command)
                return None
            func_call = re.match(r'^(\w+)\s+sails\s+with\s+(.+)$', command)
            if func_call:
                func_name = func_call.group(1)
                args_str = func_call.group(2)
                args = []
                for arg in args_str.split(','):
                    arg_val = self.parse_expression(arg.strip())
                    args.append(arg_val)
                
                if func_name in self.ship_logs:
                    unboxed_args = [arg.value if isinstance(arg, PirateType) else arg for arg in args]
                    result = self.ship_logs[func_name](*unboxed_args)
                    return PirateType(result) if result is not None else None
                
                if func_name in self.pirate_crew:
                    return self.pirate_crew[func_name](self, args)
                
                raise PirateException(f"Unknown function: {func_name}")

            var_match = re.match(r'^(\w+)\s+be\s+(.+)$', command)
            if var_match:
                var_name = var_match.group(1)
                value_str = var_match.group(2)

                list_match = re.match(r'^list\s+of\s+(.+)$', value_str)
                if list_match:
                    items = [self.parse_expression(item.strip()).value for item in list_match.group(1).split(',')]
                    self.treasure_chest[var_name] = PirateType(items, 'list')
                    return None

                arith_match = re.match(r'^(.+?)\s+(plus|minus|times|divided_by|modulo|power)\s+(.+)$', value_str)
                if arith_match:
                    left = self.parse_expression(arith_match.group(1))
                    op = arith_match.group(2)
                    right = self.parse_expression(arith_match.group(3))
                    
                    left_val = left.value if isinstance(left, PirateType) else left
                    right_val = right.value if isinstance(right, PirateType) else right
                    
                    result = self.pirate_ops[op](left_val, right_val)
                    self.treasure_chest[var_name] = PirateType(result)
                    return None

                value = self.parse_expression(value_str)
                self.treasure_chest[var_name] = value
                return None

            if command.startswith('bark'):
                args = command[4:].strip()
                if not args:
                    self.pirate_print()
                    return None
                
                parsed_args = []
                for arg in re.findall(r'"[^"]*"|[^,]+', args):
                    arg = arg.strip(' ,"')
                    if arg.startswith('"') and arg.endswith('"'):
                        parsed_args.append(arg[1:-1])
                    else:
                        try:
                            parsed_arg = self.parse_expression(arg)
                            parsed_args.append(parsed_arg)
                        except PirateException:
                            parsed_args.append(arg)
                self.pirate_print(*parsed_args)
                return None



            list_append = re.match(r'^add\s+(.+)\s+to\s+(\w+)$', command)
            if list_append:
                item = self.parse_expression(list_append.group(1))
                list_name = list_append.group(2)
                lst = self.resolve_variable(list_name)
                if isinstance(lst, PirateType) and isinstance(lst.value, list):
                    lst.value.append(item.value if isinstance(item, PirateType) else item)
                    return None
                raise PirateException(f"{list_name} is not a list")

            if command == 'debug_chest':
                return self.debug_treasure_chest()

            if_match = re.match(r'^if\s+(.+?)\s+be\s+(less_than|greater_than|equals|greater_or_equal|less_or_equal)\s+(.+?)\s*,\s*then\s+(.+?)(?:\s+else\s+(.+))?$', command)
            if if_match:
                cond_left = self.parse_expression(if_match.group(1))
                comparison = if_match.group(2)
                cond_right = self.parse_expression(if_match.group(3))
                then_action = if_match.group(4)
                else_action = if_match.group(5)

                left_val = cond_left.value if isinstance(cond_left, PirateType) else cond_left
                right_val = cond_right.value if isinstance(cond_right, PirateType) else cond_right

                if self.pirate_ops[comparison](left_val, right_val):
                    return self.parse_command(then_action)
                elif else_action:
                    return self.parse_command(else_action)
                return None

            raise PirateException(f"Cannot parse command: {command}")   
        except Exception as e:
            if isinstance(e, PirateException):
                raise
            raise PirateException(str(e), line_number, f"Error in command: {command}")

    def run_script(self, filename: str):
        try:
            with open(filename, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line:
                        try:
                            result = self.parse_command(line, line_num)
                            if result and not isinstance(result, str):
                                print(result)
                        except PirateException as e:
                            print(e)
                        except Exception as e:
                            print(f"Error on line {line_num}: {e}")
        except FileNotFoundError:
            print(f"No script found at {filename}")
        except Exception as e:
            print(f"Arrr! Something went wrong: {e}")
