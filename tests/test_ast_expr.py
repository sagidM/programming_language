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
                'left': ['identifier', 'x'],
                'right': {
                    'argument': {
                        'left': ['identifier', 'another_variable'],
                        'right': ['identifier', 'y'],
                        'operation': '+'
                    },
                    'operation': '-'
                },
                'operation': '*'
            },
            'operation': '+'
        }
    ),
    (
        'f(g(1 + obj.prop)[3-1], second_arg) ** 1',
        {
            'left': {
                'callee': ['identifier', 'f'],
                'arguments': [
                    {
                        'accessible': {
                            'callee': ['identifier', 'g'],
                            'arguments': [
                                {
                                    'left': 1,
                                    'right': {
                                        'object': ['identifier', 'obj'],
                                        'property': ['identifier', 'prop']
                                    },
                                    'operation': '+'
                                }
                            ]
                        },
                        'index': {
                            'left': 3,
                            'right': 1,
                            'operation': '-'
                        }
                    },
                    ['identifier', 'second_arg']
                ],
            },
            'right': 1,
            'operation': '**'
        }
    ),
    (
        'a.b.c().d',
        {
            'object': {
                'callee': {
                    'object': {
                        'object': ['identifier', 'a'],
                        'property': ['identifier', 'b']
                    },
                    'property': ['identifier', 'c']
                },
                'arguments': []
            },
            'property': ['identifier', 'd']
        }
    ),
    (
        '(x+y)().prop[1][q[2]](0)',
        {
            'callee': {
                'accessible': {
                    'accessible': {
                        'object': {
                            'callee': {
                                'left': ['identifier', 'x'],
                                'right': ['identifier', 'y'],
                                'operation': '+'
                            },
                            'arguments': []
                        },
                        'property': ['identifier', 'prop']
                    },
                    'index': 1
                },
                'index': {
                    'accessible': ['identifier', 'q'],
                    'index': 2
                }
            },
            'arguments': [0]
        }
    )
)

class TestAST_expr(unittest.TestCase):
    def test_expr(self):
        for expression_param in expression_params:
            expr, ast_as_dict_expected = expression_param
            builder = SyntaxTreeBuilder(Lexer(expr).lex())
            ast_as_dict_actual = convert_to_dict(builder.expr())
            self.assertDictEqual(ast_as_dict_expected, ast_as_dict_actual)

if __name__ == '__main__':
    unittest.main()
