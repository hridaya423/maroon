"""Function representation for the Maroon interpreter."""
from typing import List, Any, Optional

from .exceptions import PirateException
from .types import PirateType

class PirateFunction:
    def __init__(self, name: str, params: List[str], body: List[str], 
                 return_type: Optional[str] = None, docstring: Optional[str] = None):
        self.name = name
        self.params = params
        self.body = body
        self.return_type = return_type
        self.docstring = docstring

    def __call__(self, interpreter, args: List[Any]) -> Any:
        if len(args) != len(self.params):
            raise PirateException(
                f"Arrr! {self.name} expects {len(self.params)} arguments, " +
                f"but got {len(args)}!",
                context=f"Parameters: {self.params}"
            )

        interpreter.push_scope()

        try:
            for param, arg in zip(self.params, args):
                interpreter.treasure_chest[param] = (
                    arg if isinstance(arg, PirateType) 
                    else PirateType(arg)
                )
            
            result = None
            for line in self.body:
                result = interpreter.parse_command(line)
                
                import re
                return_match = re.match(r'^return (.+)$', line.strip())
                if return_match:
                    result = interpreter.parse_expression(return_match.group(1))
                    break
            
            return result

        except Exception as e:
            raise PirateException(
                f"Mutiny in function {self.name}!",
                context=str(e)
            )
        finally:
            interpreter.pop_scope()