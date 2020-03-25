from src.lexer import is_number_token
# expr         => shiftable ((<< | >>) shiftable)*
# shiftable    => term ((+ | -) term)*
# term         => unary ((* | / | // | %) unary)*
# unary        => (~ | + | -) unary | factor [** unary]
# factor       => (LPAREN expr RPAREN | literal | IDENTIFIER) [member | call | subscript]*
# member       => . IDENTIFIER
# call         => LPAREN [expr [, expr]*] RPAREN
# subscript    => LSBRACKET expr RSBRACKET
# literal      => NUM | STRING

# terminable parts:
# NUM          => int or double C-like number: 4, 1.5, 2., .7, 2.4e-2
# IDENTIFIER   => C-like identifier including non-ASCII letters: s, ё_2_
# LPAREN       => (
# RPAREN       => )
# LSBRACKET    => [
# RSBRACKET    => ]

class BinaryExpression:
    def __init__(self, left, right, operator):
        self.left = left
        self.right = right
        self.operator = operator

    def __str__(self):
        return f'< {self.left} ({self.operator}) {self.right} >'

class MemberExpression:
    def __init__(self, object, property):
        self.object = object
        self.property = property

class Call:
    def __init__(self, callee, arguments):
        self.callee = callee
        self.arguments = arguments

class Substript:
    def __init__(self, accessible, index):
        self.accessible = accessible
        self.index = index

class UnaryExpression:
    def __init__(self, operator, argument):
        self.operator = operator
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

    def parse_body(self):
        typ = self.current_token()[0]
        statements = []
        while typ != 'TERMINATE_TOKEN':
            if typ == 'fn':
                statements.append(self.function_block())
            elif typ == 'if':
                statements.append(self.if_block())
            elif typ in ';\n':
                self.advance_token()
            else:
                statements.append(self.expr())
            typ = self.current_token()[0]
        return statements

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
        node = self.unary()
        ct = self.current_token()
        while ct[0] in '*//%':
            self.advance_token()
            node = BinaryExpression(node, self.unary(), ct[0])
            ct = self.current_token()
        return node

    def unary(self):
        ct = self.current_token()
        if ct[0] in '~+-':
            self.advance_token()
            return UnaryExpression(ct[0], self.unary())

        node = self.factor()
        ct = self.current_token()
        if ct[0] == '**':
            self.advance_token()
            node = BinaryExpression(node, self.unary(), '**')
        return node

    def factor(self):
        # literal => (LPAREN expr RPAREN | literal) [call | subscript]*
        ct = self.current_token()
        self.advance_token()
        if ct[0] == '(':
            node = self.expr()
            assert self.current_token()[0] == ')'
            self.advance_token()
        elif ct[0] == 'identifier':
            node = ct
        elif ct[0] == 'TERMINATE_TOKEN':
            raise SyntaxError('Unexpected TERMINATE_TOKEN')
        else:
            # TODO: add another literals
            if ct[0] not in ('int_value', 'float_value', 'exponent_value'):
                raise NotImplementedError(f'Unknown literal: {ct[0]}')
            node = Number(ct)
        
        while True:
            ct = self.current_token()
            if ct[0] == '.':    # obj.prop
                self.advance_token()
                prop = self.current_token()
                if prop[0] != 'identifier':
                    raise SyntaxError(str(prop[1]) + ' is given, but identifier is expected')
                node = MemberExpression(node, prop)
                self.advance_token()
            elif ct[0] == '(':  # f()
                self.skip_token('(')
                node = Call(node, self.call_arguments())
                self.skip_token(')', 'There is no closing bracket ")" for the function call')
            elif ct[0] == '[':  # arr[index]
                self.skip_token('[')
                node = Substript(node, self.expr())
                self.skip_token(']', 'There is no closing square bracket "]" for the subscript')
            else:
                return node

    def call_arguments(self):
        args = []
        if self.current_token()[0] == ')':
            return args
        args.append(self.expr())    # no comma before 1st arg
        while self.current_token()[0] != ')':
            self.skip_token(',', 'Arguments should be separated by commas')
            args.append(self.expr())
        return args

    def literal(self):
        ct = self.current_token()
        if is_number_token(ct):
            self.advance_token()
            return Number(ct)

    def expr_in_parenthesis(self):
        self.skip_token('(')
        node = self.expr()
        self.skip_token(')', 'Closing bracket is not found')
        return node

    def skip_token(self, token: str, msg: str = ''):
        if self.current_token()[0] != token:
            raise SyntaxError(msg + '; given token: ' + str(self.current_token()))
        self.advance_token()


# 1+2*3 => +(1,*(2,3))
def build_abstract_tree(lex_result):
    return SyntaxTreeBuilder(lex_result).parse_body()
