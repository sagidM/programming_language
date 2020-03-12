from sys import argv
from argparse import ArgumentParser
from src.lexer import Lexer
from src.abstract_tree import build_abstract_tree
from src.helpers.object_converter import to_pretty_format
from src.executor import execute_ast_expression

def read_from_file(filename):
    with open(filename) as f:
        return f.read()

def run(args):
    if args.oneline:
        code = args.oneline
    else:
        code = read_from_file(args.filename)

    tokens = Lexer(code).lex()
    if args.output == 'lex':
        return tokens
    ast = build_abstract_tree(tokens)
    if args.output == 'ast':
        return to_pretty_format(ast)
    return execute_ast_expression(ast)


parser = ArgumentParser()
parser.add_argument('-o', '--output',
    choices=('lex', 'ast', 'result'),
    default='result',
    help='Outputs either tokens or AST')
parser.add_argument('--oneline', default=None, help='Executes a line instead of a file')
parser.add_argument('filename', default=None, nargs='?', help='File that should be run')
args = parser.parse_args(argv[1:])

print(run(args))
