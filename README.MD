![Maroon Logo](https://github.com/hridaya423/maroon/blob/master/maroon-logo.png)

Maroon is a pirate-themed programming language that makes coding as adventurous as sailing the high seas! Written in Python, it features a unique syntax inspired by pirate parlance while maintaining functional programming capabilities.

## Features

- Pirate-themed syntax that's both fun and functional
- Built-in type system with support for numbers, strings, booleans, and lists
- Function definitions using `voyage` keyword
- Rich set of mathematical and logical operations
- Built-in debugging tools
- Scope management with variable stacking
- Exception handling with pirate-flavored error messages

## Core Syntax

### Variable Assignment
```
treasure be 42
message be "Ahoy, world!"
```

### Arithmetic Operations
- `plus`: Addition
- `minus`: Subtraction
- `times`: Multiplication
- `divided_by`: Division
- `modulo`: Modulus
- `power`: Exponentiation

### Built-in Functions
- `bark`: Print output
- `count_booty`: Length function
- `plunder`: Maximum value
- `abandon`: Minimum value
- `debug_chest`: Debug current scope
- `sqrt`, `abs`, `round`: Mathematical operations
- `to_int`, `to_float`, `to_str`: Type conversion

### Function Definition
```
voyage greet(name):
    bark "Ahoy," name
end voyage
```

### Lists
```
crew be list of "Jack", "Anne", "Mary"
add "Blackbeard" to crew
```

### Conditionals
```
if gold be greater_than 100, then bark "Rich!" else bark "Poor!"
```

## Error Handling

The interpreter provides detailed error messages through the `PirateException` class, helping developers navigate through rough seas of debugging.

## Development

The interpreter is built with clean, modular Python code featuring:
- Regular expression parsing
- Robust type system
- Comprehensive operator support
- Modular function handling

## Getting Started

1. Clone the repository
2. Run Maroon scripts with `.maroon` extension
3. Start writing your pirate-themed programs!

Example:
```
treasure be 42
bark "Me treasure chest holds" treasure "gold pieces!"
```
4. Run the script with:
python main.py yourfilename
or python main.py for the shell

## License

MIT License! Steal at yer own risk 💀🏴‍☠️

## Contributing

Join our crew! Contributions are welcome through pull requests.
