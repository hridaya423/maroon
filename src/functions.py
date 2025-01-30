from typing import List, Any, Optional

from .exceptions import PirateException
from .types import PirateType

class PirateFunction:
    def __init__(self, name: str, params: List[tuple], body: List[str]):
        self.name = name
        self.params = params
        self.body = body

    def __call__(self, interpreter, args: List[Any]) -> Any:
        required_params = sum(1 for p in self.params if p[1] is None)
        
        if len(args) < required_params:
            raise PirateException(
                f"Arrr! {self.name} expects at least {required_params} arguments, got {len(args)}",
                context=f"Parameters: {[p[0] for p in self.params]}"
            )
        if len(args) > len(self.params):
            raise PirateException(
                f"Arrr! {self.name} expects at most {len(self.params)} arguments, got {len(args)}",
                context=f"Parameters: {[p[0] for p in self.params]}"
            )
        combined_args = []
        for i in range(len(self.params)):
            param_name, default_value = self.params[i]
            combined_args.append(args[i] if i < len(args) else default_value)
        interpreter.push_scope()
        try:
            for param_info, arg in zip(self.params, combined_args):
                param_name = param_info[0]
                if arg is None:
                    raise PirateException(f"Missing value for parameter: {param_name}")
                interpreter.treasure_chest[param_name] = (
                    arg if isinstance(arg, PirateType) 
                    else PirateType(arg)
                )
            result = None
            for line in self.body:
                line = line.strip()
                if line.startswith('return'):
                    result = interpreter.parse_expression(line[6:].strip())
                    break
                result = interpreter.parse_command(line)
            return result
        except Exception as e:
            raise PirateException(
                f"Mutiny in function {self.name}!",
                context=str(e)
            )
        finally:
            interpreter.pop_scope()