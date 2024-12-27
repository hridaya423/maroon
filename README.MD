![Maroon Logo](https://cloud-r5gvnkecb-hack-club-bot.vercel.app/0maroon_logo-removebg-preview.png)

Maroon is a pirate-themed programming language that makes coding as adventurous as sailing the high seas! Written in Python, it features a unique syntax inspired by pirate parlance while maintaining functional programming capabilities.

## Update v1.1
### New Control Structures

#### While loops with comparison operators

`while counter be less_than 3 bark counter`

#### Plunder loops (foreach)

`plunder each coin from treasure_chest bark coin`

#### Repeat loops

`repeat 3 times bark "BOOM!"`

### Choose statements (switch/case)
```
choose x:
    case 1: bark "one"
    default: bark "unknown"
end choose
```

### Error Handling
```
brace for impact:
    bark "Dangerous waters"
if capsized, bark "Error!"
```

### Functional Operations

- List comprehension: `list of 1, 2, 3 where each times 2`
- Filter: `coins where it greater_than 5`
- Reduce: `reduce coins with result plus it`

### String Operations

- Upper/lower case: `"hello" upper`
- Split/join: `"hello world" split " "`

### Custom Dialects
```
dialect Caribbean:
    "shout" be "bark"
    "expedition" be "voyage"
end dialect
```
### New Math & Randomization features
```
bark roll_dice sails with 20
bark random_float sails with
bark random_float sails with 10, 20

crew be list of 1, 2, 3, 4, 5
bark random_pick sails with crew
bark random_sample sails with crew, 3
bark normal_random sails with

# Math operations 
x be 5
bark factorial sails with x

angle be 3.14159
bark sin sails with angle
bark cos sails with angle
bark tan sails with angle

bark exp sails with 2
bark log sails with 10
bark log sails with 8, 2

# Statistical operations
numbers be list of 2, 4, 6, 8, 10
bark mean sails with numbers
bark median sails with numbers
bark sum sails with numbers

# Gaming functions
bark flip_coin sails with
bark roll_multiple sails with 3, 6
bark roll_multiple sails with 2, 20
```

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
