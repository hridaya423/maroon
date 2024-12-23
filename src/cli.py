"""Command-line interface for Maroon."""
import sys
import traceback
from .interpreter import PirateInterpreter
from .exceptions import PirateException

def run_interactive_shell(interpreter: PirateInterpreter):
    print("Maroon Shell!")
    print("Type 'hoist anchor' to exit")
    
    while True:
        try:
            command = input("Pirate> ").strip()
            
            if command == 'hoist anchor':
                print("Farewell, ye scurvy programmer!")
                break
            
            result = interpreter.parse_command(command)
            if result is not None:
                print(result)
        
        except PirateException as e:
            print(e)
        except Exception as e:
            print(f"Unexpected error: {traceback.format_exc()}")

def run_script(interpreter: PirateInterpreter, filename: str):
    try:
        interpreter.run_script(filename)
    except FileNotFoundError:
        print(f"Arrr! No treasure map found at {filename}")
    except Exception as e:
        print(f"Arrr! Something went wrong: {e}")

def main():
    interpreter = PirateInterpreter()

    if len(sys.argv) > 1:
        run_script(interpreter, sys.argv[1])
    else:
        run_interactive_shell(interpreter)

if __name__ == "__main__":
    main()