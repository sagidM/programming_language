import json
import unittest
from src.lexer import Lexer
from src.abstract_tree import SyntaxTreeBuilder, Number

class SimpleEncoder(json.JSONEncoder):
    def default(self, obj):
        if type(obj) is Number:
            typ, value = obj.token
            if typ == 'int_value':
                return int(value)
            if typ == 'float_value':
                return float(value)
            return value
        return obj.__dict__ 

class TestAST(unittest.TestCase):
    def test_expr(self):
        code = '1 ** 2 ** 5'
        builder = SyntaxTreeBuilder(Lexer(code).lex())
        res = builder.expr()
        print(code)
        print('Abstract Syntax Tree')
        print(json.loads(json.dumps(SimpleEncoder(indent=2).encode(res))))
        # print(json.dumps(res.__dict__))

if __name__ == '__main__':
    unittest.main()
