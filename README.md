# Interpreter for Programming Language

This is an interpreter written in Python for a programming language I am building.

# Description
It is a dynamic indentation-sensitive language that is inspired by Python, Haskell, CoffeeScript and some other languages.

# Motivation
I am a developer who had a desire to build my own language since I began programming. Although the realization of meaninglessness to create yet another programming language has come quite early, I eventually decided that I should build a language chasing 2 goals: to gain deep knowledge in compilers and it just funny.

# Run interpreter in 3 steps
> Notice, it is assumed that Python3 is installed.

Clone the repo, cd in the directory and run **repl**.
```bash
git clone https://github.com/sagidM/programming_language.git
cd programming_language
# Either one
./repl          # Linux / MacOS
python3 repl    # Any
```
```bash
```

# Development
You can get Abstract Syntax Tree or Tokens from a file or a line or code.

But it is recommended to run all the commands from a virtual environment, so to create one, simply run
```bash
pip3 install virtualenv
virtualenv name_of_venv
```

Activate your environment

Linux / Mac OS
```bash
source name_of_venv/bin/activate
```
Windows
```bash
name_of_venv\bin\activate
```

To deactivate, run `deactivate`

# Examples
Once you are in virtual environment, you can run a file/line, or get tokens or AST from it.
```bash
$ python src/main.py -o ast --oneline "1 + 2"
# output
[
  {
    "left": 1,
    "right": 2,
    "operator": "+"
  }
]

$ python src/main.py -o lex --oneline "1 + 2"
# output
[('int_value', '1'), ('+', '+'), ('int_value', '2'), ('TERMINATE_TOKEN', '')]
```
If you do not pass `--oneline`, the string `"1 + 2"` will be interpreted as a name of the file that should be executed.

An optional argument `-o` or `--output` has 3 values, which denote:
- `lex` -- to output lexemes
- `ast` -- to output Abstract Syntax Tree
- `result` (default) -- to output just a result of the execution the file/string as a program line by line

One more example
```bash
$ python src/main.py -o ast --oneline "1+2*3; 1+2**3"
[
  {
    "left": 1,
    "right": {
      "left": 2,
      "right": 3,
      "operator": "*"
    },
    "operator": "+"
  },
  {
    "left": 1,
    "right": {
      "left": 2,
      "right": 3,
      "operator": "**"
    },
    "operator": "+"
  }
]
```

# Reach me out
If you want to build your own programming language and have questions, or would like to discuss something, I encourage you reaching me out. I will enjoy sharing my knowledge or getting your advice.  
Appreciate you made it this far.
