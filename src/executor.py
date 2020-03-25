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
        return binary_operations[root.operator](left, right)
    if tp is UnaryExpression:
        num = execute_ast_expression(root.argument)
        return unary_operations[root.operator](num)
    if tp is Number:
        number_type, number_value = root.token
        if number_type == 'int_value':
            return int(number_value)
        return float(number_value)
    raise TypeError('Unknown type: ' + str(tp))

def execute_from_code(code):
    lex_result = lex(code)
    tree_statements = build_abstract_tree(lex_result)
    result = []
    for tree in tree_statements:
        result.append(execute_ast_expression(tree))
    return result

def lex(code):
    return Lexer(code).lex()
