from src.lexer import is_number_token
# expr   => term [(+ | -) term]*
# term   => factor [(* | / | // | ^) factor]*
# factor => num

class BinaryOperation:
    def __init__(self, left, right, operation):
        self.left = left
        self.right = right
        self.operation = operation

    def __str__(self):
        return f'< {self.left} ({self.operation}) {self.right} >'

class Number:
    def __init__(self, token):
        self.token = token
    def __str__(self):
        return f'Number({self.token})'

class SyntaxTreeBuilder:
    def __init__(self, lex_result):
        self.tokens = lex_result
        self.current_token_index = 0

    def current_token(self):
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None
    def advance_token(self):
        self.current_token_index += 1

    def expr(self):
        node = self.term()
        ct = self.current_token()
        while ct and ct[0] in '+-':
            self.advance_token()
            node = BinaryOperation(node, self.term(), ct[0])
            ct = self.current_token()
        return node
    def term(self):
        node = self.factor()
        ct = self.current_token()
        while ct and ct[0] in '*//^':
            self.advance_token()
            node = BinaryOperation(node, self.factor(), ct[0])
            ct = self.current_token()
        return node
    def factor(self):
        ct = self.current_token()
        self.advance_token()
        if is_number_token(ct):
            return Number(ct)
        if ct[0] == '(':
            node = self.expr()
            assert self.current_token()[0] == ')'
            self.advance_token()
            return node
        raise ValueError('Unexpected token: ' + ct[0])

# 1+2*3 => +(1,*(2,3))
def build_abstract_tree(lex_result):
    for token_type, token_value in lex_result:
        token_type