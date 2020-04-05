import unittest
import json
from src.lexer import Lexer
from src.abstract_tree import SyntaxTreeBuilder
from src.helpers.object_converter import convert_to_dict, to_pretty_format


expression_params = (
    (
        '1+4;4-6',
        [
            {
                'left': 1,
                'right': 4,
                'operator': '+'
            },
            {
                'left': 4,
                'right': 6,
                'operator': '-'
            },
        ]
    ),
)

class TestAST_multilines(unittest.TestCase):
    def test_multilines(self):
        for expression_param in expression_params:
            expr, body_expected = expression_param
            builder = SyntaxTreeBuilder(Lexer(expr).lex())
            body_actual = convert_to_dict(builder.parse_body())
            self.assertEqual(body_expected, body_actual)

if __name__ == '__main__':
    unittest.main()
