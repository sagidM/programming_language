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

class ExecutionContext:
    def __init__(self):
        self._identifiers = dict()

    def get_identifier(self, name: str):
        return self._identifiers[name]

    def set_identifier(self, name, value):
        self._identifiers[name] = value

    def has_identifier(self, name):
        return name in self._identifiers

    def execute_ast_expression(self, root):
        tp = type(root)
        if tp is BinaryExpression:
            # The only case when right value must be executed first, on the = operator
            if root.operator == '=':
                right = self.execute_ast_expression(root.right)
                self.set_identifier(root.left.name, right)
                return right
            left = self.execute_ast_expression(root.left)
            right = self.execute_ast_expression(root.right)
            return binary_operations[root.operator](left, right)
        if tp is UnaryExpression:
            num = self.execute_ast_expression(root.argument)
            return unary_operations[root.operator](num)
        if tp is Number:
            number_type, number_value = root.token
            if number_type == 'int_value':
                return int(number_value)
            return float(number_value)
        if type(root) is Identifier:
            if not self.has_identifier(root.name):
                raise NameError(f'The identifier "{root.name}" is not defined')
            return self.get_identifier(root.name)
        raise TypeError('Unknown type: ' + str(tp))

    def execute_from_code(self, code: str):
        lex_result = lex(code)
        tree_statements = build_abstract_tree(lex_result)
        result = []
        for tree in tree_statements:
            result.append(self.execute_ast_expression(tree))
        return result

def lex(code):
    return Lexer(code).lex()
