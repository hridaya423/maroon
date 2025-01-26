"""Core interpreter for Maroon"""
import re
import math
import operator
from typing import Any, List
from random import uniform, choice, sample, gauss, randint, shuffle as random_shuffle
from math import sin, cos, tan, log, exp, factorial

from .exceptions import PirateException
from .types import PirateType   
from .functions import PirateFunction
from .eastereggs import PirateEasterEggs
from .dialects import DialectManager
from .firstmate import FirstMate
from .patterns import PatternHandler
from .loops import LoopHandler
from .switchcase import SwitchCaseHandler
from .trycatch import TryCatchHandler

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
            'roll_dice': lambda sides=6: randint(1, sides.value if isinstance(sides, PirateType) else sides),
            'random_float': self.pirate_random_float,
            'random_pick': lambda lst: choice(lst.value if isinstance(lst, PirateType) else lst),
            'flip_coin': self.pirate_flip_coin,
            'random_sample': self.pirate_random_sample,
            'normal_random': lambda mu=0, sigma=1: gauss(
                mu.value if isinstance(mu, PirateType) else mu,
                sigma.value if isinstance(sigma, PirateType) else sigma
            ),
            'log': lambda x, base=math.e: log(
                x.value if isinstance(x, PirateType) else x,
                base.value if isinstance(base, PirateType) else base
            ),
            'roll_multiple': lambda num_dice=1, sides=6: [
                randint(1, sides.value if isinstance(sides, PirateType) else sides)
                for _ in range(num_dice.value if isinstance(num_dice, PirateType) else num_dice)
            ],
            'factorial': lambda x: factorial(int(x.value if hasattr(x, 'value') else x)),
            'sin': lambda x: sin(float(x.value if hasattr(x, 'value') else x)),
            'cos': lambda x: cos(float(x.value if hasattr(x, 'value') else x)),
            'tan': lambda x: tan(float(x.value if hasattr(x, 'value') else x)),
            'exp': lambda x: exp(float(x.value if hasattr(x, 'value') else x)),
            'mean': lambda lst: sum(lst.value if hasattr(lst, 'value') else lst) / len(lst.value if hasattr(lst, 'value') else lst),
            'median': lambda lst: sorted(lst.value if hasattr(lst, 'value') else lst)[len(lst.value if hasattr(lst, 'value') else lst) // 2],
            'sum': lambda lst: sum(lst.value if hasattr(lst, 'value') else lst),
            'map': self.pirate_map,
            'filter': self.pirate_filter,
            'reduce': self.pirate_reduce,
            'shuffle': self.pirate_shuffle,
            'weighted_choice': self.pirate_weighted_choice,
            'shout': self.pirate_shout,
            'split_loot': self.pirate_split,
            'join_crew': self.pirate_join,
        }
        self.pirate_crew = {}
        self.pirate_ops = {
            'modulo': operator.mod,
            'times': operator.mul,
            'divided_by': operator.truediv,
            'plus': operator.add,
            'minus': operator.sub,
            'equals': operator.eq,
            'greater_than': operator.gt,
            'less_than': operator.lt,
            'power': operator.pow,
            'greater_or_equal': operator.ge,
            'less_or_equal': operator.le,
            'and': lambda x, y: x and y,
            'or': lambda x, y: x or y,
            'not': lambda x: not x,
        }
        self.easter_eggs = PirateEasterEggs()
        self.easter_eggs.interpreter = self
        self.dialect_manager = DialectManager()
        self.first_mate = FirstMate(self)
        self.first_mate_active = False
        self.pattern_handler = PatternHandler(self)
        self.loop_handler = LoopHandler(self)
        self.switch_handler = SwitchCaseHandler(self)
        self.try_catch_handler = TryCatchHandler(self)
        
    def pirate_flip_coin(self):
        return choice(['heads', 'tails'])
    def pirate_shuffle(self, lst):
        if isinstance(lst, PirateType):
            lst_value = lst.value
        else:
            lst_value = lst
        shuffled = sample(lst_value, len(lst_value))
        return shuffled
    def pirate_shout(self, s):
        if isinstance(s, PirateType):
            s_val = s.value
        else:
            s_val = s
            
        if not isinstance(s_val, str):
            raise PirateException("Shout expects a string treasure!")
            
        return PirateType(s_val.upper(), 'string')

    def pirate_split(self, s, sep=None):
        if isinstance(s, PirateType):
            s_val = s.value
        else:
            s_val = s
        if not isinstance(s_val, str):
            raise PirateException("Ye can only split text loot!")
        sep_val = None
        if sep is not None:
            if isinstance(sep, PirateType):
                sep_val = sep.value
            else:
                sep_val = sep
            if not isinstance(sep_val, str):
                raise PirateException("Splitter must be text!")
        split_list = s_val.split(sep_val) if sep_val else s_val.split()
        pirate_list = [PirateType(item, 'string') for item in split_list]
        return PirateType(pirate_list, 'list')
    def pirate_join(self, items, sep):
        if isinstance(items, PirateType):
            items_val = items.value
        else:
            items_val = items
        if not isinstance(items_val, list):
            raise PirateException("Ye need a crew list to join!")
        if isinstance(sep, PirateType):
            sep_val = sep.value
        else:
            sep_val = sep
        if not isinstance(sep_val, str):
            raise PirateException("Crew bond must be text!")
        str_items = [str(item.value if isinstance(item, PirateType) else item) 
                    for item in items_val]
        return PirateType(sep_val.join(str_items), 'string')
    def pirate_weighted_choice(self, items, weights):
        items_list = items.value if isinstance(items, PirateType) else items
        weights_list = weights.value if isinstance(weights, PirateType) else weights
        if len(items_list) != len(weights_list):
            raise PirateException("Items and weights must be of the same length")
        total = sum(weights_list)
        r = uniform(0, total)
        cumulative = 0
        for item, weight in zip(items_list, weights_list):
            if r < cumulative + weight:
                return item
            cumulative += weight
        return items_list[-1]
    def pirate_random_float(self, *args):
        if len(args) == 0:
            return uniform(0, 1)
        elif len(args) == 1:
            return uniform(0, args[0])
        elif len(args) == 2:
            return uniform(args[0], args[1])
        else:
            raise PirateException("random_float expects 0-2 arguments")
    def pirate_random_sample(self, lst, k):
        lst_value = lst.value if isinstance(lst, PirateType) else lst
        k_value = k.value if isinstance(k, PirateType) else k
        return sample(lst_value, k_value)
    
    
    def pirate_map(self, collection, func_ref):
        if isinstance(collection, PirateType):
            collection = collection.value
        if not isinstance(collection, list):
            raise PirateException("Map requires a list as the first argument")
        if isinstance(func_ref, PirateType):
            func_ref = func_ref.value
        if not isinstance(func_ref, str):
            raise PirateException("Function reference must be a string")
        
        if func_ref in self.ship_logs:
            func = self.ship_logs[func_ref]
            mapped = []
            for item in collection:
                try:
                    result = func(item)
                    mapped.append(result)
                except Exception as e:
                    raise PirateException(f"Error in map function {func_ref}: {e}")
            return mapped
        elif func_ref in self.pirate_crew:
            func = self.pirate_crew[func_ref]
            if len(func.params) < 1:
                raise PirateException(f"Function {func_ref} must take at least one parameter for map")
            mapped = []
            for item in collection:
                arg = PirateType(item)
                result = self.execute_function(func_ref, [arg])
                mapped_value = result.value if isinstance(result, PirateType) else result
                mapped.append(mapped_value)
            return mapped
        else:
            raise PirateException(f"Function {func_ref} not found")

    def pirate_filter(self, collection, func_ref):
        if isinstance(collection, PirateType):
            collection = collection.value
        if not isinstance(collection, list):
            raise PirateException("Filter requires a list as the first argument")
        if isinstance(func_ref, PirateType):
            func_ref = func_ref.value
        if not isinstance(func_ref, str):
            raise PirateException("Function reference must be a string")
        
        filtered = []
        if func_ref in self.ship_logs:
            func = self.ship_logs[func_ref]
            for item in collection:
                try:
                    result = func(item)
                    if result:
                        filtered.append(item)
                except Exception as e:
                    raise PirateException(f"Error in filter function {func_ref}: {e}")
        elif func_ref in self.pirate_crew:
            func = self.pirate_crew[func_ref]
            if len(func.params) < 1:
                raise PirateException(f"Function {func_ref} must take at least one parameter for filter")
            for item in collection:
                arg = PirateType(item)
                result = self.execute_function(func_ref, [arg])
                condition = result.value if isinstance(result, PirateType) else result
                if condition:
                    filtered.append(item)
        else:
            raise PirateException(f"Function {func_ref} not found")
        return filtered

    def pirate_reduce(self, collection, func_ref, initial=None):
        if isinstance(collection, PirateType):
            collection = collection.value
        if not isinstance(collection, list):
            raise PirateException("Reduce requires a list as the first argument")
        if isinstance(func_ref, PirateType):
            func_ref = func_ref.value
        if not isinstance(func_ref, str):
            raise PirateException("Function reference must be a string")
        if initial is None:
            if not collection:
                raise PirateException("Reduce of empty collection with no initial value")
            accumulator = collection[0]
            start_index = 1
        else:
            accumulator = initial.value if isinstance(initial, PirateType) else initial
            start_index = 0
        if func_ref in self.ship_logs:
            func = self.ship_logs[func_ref]
            for item in collection[start_index:]:
                try:
                    accumulator = func(accumulator, item)
                except Exception as e:
                    raise PirateException(f"Error in reduce function {func_ref}: {e}")
        elif func_ref in self.pirate_crew:
            func = self.pirate_crew[func_ref]
            if len(func.params) < 2:
                raise PirateException(f"Function {func_ref} must take at least two parameters for reduce")
            for item in collection[start_index:]:
                args = [PirateType(accumulator), PirateType(item)]
                result = self.execute_function(func_ref, args)
                if isinstance(result, PirateType):
                    accumulator = result.value
                else:
                    accumulator = result
        else:
            raise PirateException(f"Function {func_ref} not found")
        return accumulator
    def parse_expression(self, expr: str) -> Any:
        expr = expr.strip()
        if expr.startswith('(') and expr.endswith(')'):
            args = []
            current_arg = []
            paren_depth = 0
            for char in args_str:
                if char == '(': paren_depth += 1
                if char == ')': paren_depth -= 1
                if char == ',' and paren_depth == 0:
                    args.append(''.join(current_arg).strip())
                    current_arg = []
                else:
                    current_arg.append(char)
            if current_arg:
                args.append(''.join(current_arg).strip())
                return self.parse_expression(expr[1:-1])
        comparison_match = re.match(
            r'^(.+?)\s+(equals|greater_than|less_than)\s+(.+)$', 
            expr
        )
        if comparison_match:
            left = self.parse_expression(comparison_match.group(1))
            op = comparison_match.group(2)
            right = self.parse_expression(comparison_match.group(3))
            left_val = left.value if isinstance(left, PirateType) else left
            right_val = right.value if isinstance(right, PirateType) else right
            return PirateType(
                self.pirate_ops[op](left_val, right_val),
                'boolean'
            )
        for op in ['modulo', 'times', 'divided_by', 'power', 'plus', 'minus']:
            pattern = r'^(.*?)\s+({})\s+(.*)$'.format(re.escape(op))
            arith_match = re.match(pattern, expr)
            if arith_match:
                left = self.parse_expression(arith_match.group(1))
                right = self.parse_expression(arith_match.group(3))
                left_val = left.value if isinstance(left, PirateType) else left
                right_val = right.value if isinstance(right, PirateType) else right
                
                if op == 'modulo' and right_val == 0:
                    raise PirateException("Modulo by zero!")
                    
                return PirateType(self.pirate_ops[op](left_val, right_val))
        func_call = re.match(r'^(\w+)\s+sails\s+with(?:\s+(.+))?$', expr)
        if func_call:
            func_name = func_call.group(1)
            args_str = func_call.group(2) or ''
            args = []
            for arg in args_str.split(','):
                arg = arg.strip()
                if arg:
                    parsed_arg = self.parse_expression(arg)
                    args.append(parsed_arg)
            
            if func_name in self.ship_logs:
                unboxed_args = [arg.value if isinstance(arg, PirateType) else arg for arg in args]
                result = self.ship_logs[func_name](*unboxed_args)
                return PirateType(result)
            
            if func_name in self.pirate_crew:
                return self.execute_function(func_name, args)
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
    def kill_first_mate(self):
        self.first_mate_active = False
        print("First Mate has walked the plank!")
    def revive_first_mate(self):
        self.first_mate_active = True
        print("First Mate has returned from Davy Jones' locker!")
    def execute_function(self, func_name: str, args: List[Any]) -> Any:
        if func_name in self.pirate_crew:
            self.push_scope()
            func = self.pirate_crew[func_name]

            combined_args = []
            for i, param_info in enumerate(func.params):
                param_name, default_value = param_info
                if i < len(args):
                    combined_args.append(args[i])
                else:
                    combined_args.append(default_value)

            for param_info, arg in zip(func.params, combined_args):
                param_name = param_info[0]
                self.treasure_chest[param_name] = arg
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
        message = " ".join(str(arg) for arg in printed_args)
        print(message)
        if self.easter_eggs.parrot_mode:
            print(message)

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
            
            dialect_result = self.dialect_manager.parse_dialect_command(command)
            if dialect_result is None:  
                return None
              
            command = dialect_result
            
            processed_command = self.pattern_handler.handle_pattern(command)
            if processed_command is None:
                return None
            
            if command.strip() == "kill first mate":
                return self.kill_first_mate()
            if command.strip() == "revive first mate":
                return self.revive_first_mate()
            
            if self.easter_eggs.check_for_easter_eggs(command):
                return None
            
            loop_result = self.loop_handler.handle_loop(command)
            if loop_result is True:
                return None
            
            if self.switch_handler.handle_switch(command):
                return None
            if self.switch_handler.handle_case(command):
                return None
            if self.switch_handler.handle_default(command):
                return None
            if self.switch_handler.handle_end_switch(command):
                return None
            if self.try_catch_handler.handle_try_start(command):
                return None
            if self.try_catch_handler.handle_catch(command):
                return None
            if self.try_catch_handler.collect_try_command(command):
                return None
            
            import_match = re.match(r'^import\s+(?:"([^"]+)"|(\S+))$', command)
            if import_match:
                filename = import_match.group(1) or import_match.group(2)
                if not filename.endswith('.maroon'):
                    filename += '.maroon'
                self.run_script(filename, in_global_scope=True)
                return None
            
            func_match = re.match(r'^voyage\s+(\w+)\((.*?)\):$', command)
            if func_match:
                func_name = func_match.group(1)
                params_str = func_match.group(2)
                params = []
                for p in params_str.split(','):
                    p = p.strip()
                    if not p:
                        continue
                    if ' be ' in p:
                        name_part, default_part = p.split(' be ', 1)
                        name = name_part.strip()
                        default_value = self.parse_expression(default_part.strip())
                        params.append( (name, default_value) )
                    else:
                        params.append( (p, None) )
                
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
            
            func_call = re.match(r'^(\w+)\s+sails\s+with\s*\(?(.*?)\)?$', command)
            if func_call:
                func_name = func_call.group(1)
                args_str = func_call.group(2) or ''
                args = []
                for arg in re.split(r',(?![^[]*\])', args_str):
                    arg = arg.strip()
                    if arg:
                        parsed_arg = self.parse_expression(arg)
                        args.append(parsed_arg)
                
                if func_name in self.ship_logs:
                    unboxed_args = [arg.value if isinstance(arg, PirateType) else arg for arg in args]
                    result = self.ship_logs[func_name](*unboxed_args)
                    if result is not None:
                        return PirateType(result)
                    return None
                
                if func_name in self.pirate_crew:
                    return self.pirate_crew[func_name](self, args)
                
                raise PirateException(f"Unknown function: {func_name}")
            
            guidance = None
            if self.first_mate_active:
                guidance = self.first_mate.provide_guidance(command)
                if guidance:
                    print(guidance)
            
            var_match = re.match(r'^(\w+)\s+be\s+(.+)$', command)
            if var_match:
                var_name = var_match.group(1)
                value_str = var_match.group(2)

                list_match = re.match(r'^list\s+of\s*\[?(.*?)\]?$', value_str)
                if list_match:
                    items = []
                    if list_match.group(1).strip():
                        items = [self.parse_expression(item.strip()).value 
                                for item in re.split(r',(?![^\[]*\])', list_match.group(1))]
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
                arg_parts = re.split(r',', args)
                i = 0
                merged_parts = []
                while i < len(arg_parts):
                    part = arg_parts[i].strip()
                    if re.search(r'\bsails\s+with\b', part):
                        merged = [part]
                        i += 1
                        while i < len(arg_parts):
                            merged.append(arg_parts[i].strip())
                            i += 1
                        merged_str = ','.join(merged)
                        merged_parts.append(merged_str)
                    else:
                        merged_parts.append(part)
                        i += 1
                for part in merged_parts:
                    if not part:
                        continue
                    try:
                        parsed_arg = self.parse_expression(part)
                        parsed_args.append(parsed_arg.value if isinstance(parsed_arg, PirateType) else parsed_arg)
                    except PirateException:
                        parsed_args.append(part)
                
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
            suggestion = self.first_mate.provide_guidance(command, e)
            if suggestion:
                print(suggestion)
                raise PirateException(str(e), line_number, f"Error in command: {command}")
            if isinstance(e, PirateException):
                raise
            raise PirateException(str(e), line_number, f"Error in command: {command}")
    def run_script(self, filename: str, in_global_scope=False):
        try:
            with open(filename, 'r') as f:
                original_scope_stack = None
                if in_global_scope:
                    original_scope_stack = self.scope_stack.copy()
                    if original_scope_stack:
                        self.scope_stack = [original_scope_stack[0]]
                    else:
                        self.scope_stack = [{}]
                try:
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
                finally:
                    if in_global_scope and original_scope_stack is not None:
                        self.scope_stack = original_scope_stack
        except FileNotFoundError:
            print(f"No script found at {filename}")
        except Exception as e:
            print(f"Arrr! Something went wrong: {e}")