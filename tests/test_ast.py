import unittest
from src.lexer import Lexer
from src.abstract_tree import SyntaxTreeBuilder

class TestAST(unittest.TestCase):
    def test_expr(self):
        code = '1 + (1 + 1)'
        builder = SyntaxTreeBuilder(Lexer(code).lex())
        res = builder.expr()
        print(code)
        print(res)

if __name__ == '__main__':
    unittest.main()
