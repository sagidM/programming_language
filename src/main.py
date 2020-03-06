from sys import argv
from src.lexer import Lexer
from src.abstract_tree import build_abstract_tree
from src.helpers.object_converter import to_pretty_format


code = argv[1]
tokens = Lexer(code).lex()
ast = build_abstract_tree(tokens)
print(to_pretty_format(ast))
