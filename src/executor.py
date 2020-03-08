from src.lexer import Lexer
from src.abstract_tree import *


binary_operations = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b,
    '//': lambda a, b: a // b,
    '%': lambda a, b: a % b,
    '**': lambda a, b: a ** b,
    '<<': lambda a, b: a << b,
    '>>': lambda a, b: a >> b,
}

unary_operations = {
    '~': lambda a: ~a,
    '+': lambda a: a,
    '-': lambda a: -a,
}

def execute_ast_expression(root):
    tp = type(root)
    if tp is BinaryExpression:
        left = execute_ast_expression(root.left)
        right = execute_ast_expression(root.right)
        return binary_operations[root.operation](left, right)
    if tp is UnaryExpression:
        num = execute_ast_expression(root.argument)
        return unary_operations[root.operation](num)
    if tp is Number:
        number_type, number_value = root.token
        if number_type == 'int_value':
            return int(number_value)
        return float(number_value)
    raise TypeError('Unknown type: ' + str(tp))

def execute_from_code(code):
    lex_result = lex(code)
    tree = build_abstract_tree(lex_result)
    return execute_ast_expression(tree)

def lex(code):
    return Lexer(code).lex()
