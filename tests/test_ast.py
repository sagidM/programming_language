import unittest
import json
from src.lexer import Lexer
from src.abstract_tree import SyntaxTreeBuilder
from src.helpers.object_converter import convert_to_dict, to_pretty_format


expression_params = (
    (
        '1*2 + 3*4',
        {
            'left': {
                'left': 1,
                'right': 2,
                'operation': '*'
            },
            'right': {
                'left': 3,
                'right': 4,
                'operation': '*'
            },
            'operation': '+'
        }
    ),
    (
        '1 + 3 * 2 ** 4 + 5',
        {
            'left': {
                'left': 1,
                'right': {
                    'left': 3,
                    'right': {
                        'left': 2,
                        'right': 4,
                        'operation': '**'
                    },
                    'operation': '*'
                },
                'operation': '+'
            },
            'right': 5,
            'operation': '+'
        }
    ),
    (
        '(~2) ** 5 + ~4 * 3 // -1',
        {
            'left': {
                'left': {
                    'argument': 2,
                    'operation': '~'
                },
                'right': 5,
                'operation': '**'
            },
            'right': {
                'left': {
                    'left': {
                        'argument': 4,
                        'operation': '~'
                    },
                    'right': 3,
                    'operation': '*'
                },
                'right': {
                    'argument': 1,
                    'operation': '-'
                },
                'operation': '//'
            },
            'operation': '+'
        }
    ),
    (
        '1 + 2 << 5 % 3',
        {
            'left': {
                'left': 1,
                'right': 2,
                'operation': '+'
            },
            'right': {
                'left': 5,
                'right': 3,
                'operation': '%'
            },
            'operation': '<<'
        }
    ),
    (
        '5 + x * -(another_variable + y)',
        {
            'left': 5,
            'right': {
                'left': 'y',
                'right': {
                    'argument': {
                        'left': ('identifier', 'another_variable'),
                        'right': ('identifier', 'y'),
                        'operation': '+'
                    },
                    'operation': '-'
                },
                'operation': '*'
            }
        }
    )
)

class TestAST(unittest.TestCase):
    def test_expr(self):
        for expression_param in expression_params:
            expr, ast_as_dict_expected = expression_param
            builder = SyntaxTreeBuilder(Lexer(expr).lex())
            ast_as_dict_actual = convert_to_dict(builder.expr())
            self.assertDictEqual(ast_as_dict_expected, ast_as_dict_actual)

if __name__ == '__main__':
    unittest.main()
