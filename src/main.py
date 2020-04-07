from sys import argv
from argparse import ArgumentParser
from src.lexer import Lexer
from src.abstract_tree import build_abstract_tree
from src.helpers.object_converter import to_pretty_format
from src.executor import ExecutionContext

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
    ast_statements = build_abstract_tree(tokens)
    if args.output == 'ast':
        return to_pretty_format(ast_statements)

    context = ExecutionContext()
    return [context.execute_ast_expression(ast) for ast in ast_statements]


parser = ArgumentParser()
parser.add_argument('-o', '--output',
    choices=('lex', 'ast', 'result'),
    default='result',
    help='Outputs either tokens or AST')
parser.add_argument('--oneline', default=None, help='Executes a line instead of a file')
parser.add_argument('filename', default=None, nargs='?', help='File that should be run')
# TODO: fix an error when --oneline starts with "-"
args = parser.parse_args(argv[1:])

try:
    results = run(args)
    if type(results) == str:
        print(results)
    elif len(results) == 1:
        print(results[0])
    else:
        print('Result line by line:')
        for result in results:
            print('|>', result)
except SyntaxError as e:
    print('SyntaxError was thrown. If you are being tired remember to be happy :)')
    print(e)
    exit(1)
except NotImplementedError as e:
    print('This has not been implemented but it seems the author has some plans about it.')
    print(e)
    exit(1)
