from src.lexer import is_number_token
# expr        => shiftable ((<< | >>) shiftable)*
# shiftable   => term ((+ | -) term)*
# term        => factor ((* | / | // | %) factor)*
# factor      => unary [** factor]
# unary       => (~ | + | -) factor | num_or_pair
# num_or_pair => num | \( expr \)
# 

class BinaryExpression:
    def __init__(self, left, right, operation):
        self.left = left
        self.right = right
        self.operation = operation

    def __str__(self):
        return f'< {self.left} ({self.operation}) {self.right} >'

class UnaryExpression:
    def __init__(self, operation, argument):
        self.operation = operation
        self.argument = argument

class Number:
    def __init__(self, token):
        self.token = token
    def __str__(self):
        return f'Number({self.token})'

'''
Priorities:
**          Exponentiation
~x +x -x    Bitwise not, positive, negative
* / %       Multiplication, division, remainder
+ -         Addition, subtraction
<< >>       Bitwise shifts
'''
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

    def parse(self):
        ct = self.current_token()
        while ct:
            typ = ct[0]
            if typ == 'fn':
                self.function_block()
            elif typ == 'if':
                self.if_block()
            else:
                self.expr()
            ct = self.current_token()

    def function_block(self):
        raise NotImplementedError('not implemented')

    def if_block(self):
        raise NotImplementedError('not implemented')

    def lvalue(self):
        raise NotImplementedError('not implemented')

    def expr(self):
        node = self.shiftable()
        ct = self.current_token()
        while ct[0] in ('<<', '>>'):
            self.advance_token()
            node = BinaryExpression(node, self.shiftable(), ct[0])
            ct = self.current_token()
        return node

    def shiftable(self):
        node = self.term()
        ct = self.current_token()
        while ct[0] in '+-':
            self.advance_token()
            node = BinaryExpression(node, self.term(), ct[0])
            ct = self.current_token()
        return node
    def term(self):
        node = self.factor()
        ct = self.current_token()
        while ct[0] in '*//%':
            self.advance_token()
            node = BinaryExpression(node, self.factor(), ct[0])
            ct = self.current_token()
        return node

    def factor(self):
        # factor      => unary [** factor]
        node = self.unary()
        ct = self.current_token()
        if ct[0] == '**':
            self.advance_token()
            node = BinaryExpression(node, self.factor(), '**')
        return node

    def unary(self):
        # unary => (~ | + | -) factor | num_or_pair
        ct = self.current_token()
        if ct[0] in '~+-':
            self.advance_token()
            node = UnaryExpression(ct[0], self.factor())
        else:
            node = self.num_or_pair()
        return node

    def num_or_pair(self):
        # num_or_pair => num | \( expr \)
        ct = self.current_token()
        self.advance_token()
        if is_number_token(ct):
            return Number(ct)
        if ct[0] == '(':
            node = self.expr()
            assert self.current_token()[0] == ')'
            self.advance_token()
            return node
        raise ValueError('unexpected token: ' + ct[0])

# 1+2*3 => +(1,*(2,3))
def build_abstract_tree(lex_result):
    return SyntaxTreeBuilder(lex_result).expr()
