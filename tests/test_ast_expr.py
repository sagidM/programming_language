import unittest
import json
from src.lexer import Lexer
from src.abstract_syntax_tree import SyntaxTreeBuilder
from src.helpers.object_converter import convert_to_dict, to_pretty_format


expression_params = (
    (
        '1*2 + 3*4',
        {
            'left': {
                'left': 1,
                'right': 2,
                'operator': '*'
            },
            'right': {
                'left': 3,
                'right': 4,
                'operator': '*'
            },
            'operator': '+'
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
                        'operator': '**'
                    },
                    'operator': '*'
                },
                'operator': '+'
            },
            'right': 5,
            'operator': '+'
        }
    ),
    (
        '(~2) ** 5 + ~4 * 3 // -1',
        {
            'left': {
                'left': {
                    'argument': 2,
                    'operator': '~'
                },
                'right': 5,
                'operator': '**'
            },
            'right': {
                'left': {
                    'left': {
                        'argument': 4,
                        'operator': '~'
                    },
                    'right': 3,
                    'operator': '*'
                },
                'right': {
                    'argument': 1,
                    'operator': '-'
                },
                'operator': '//'
            },
            'operator': '+'
        }
    ),
    (
        '1 + 2 << 5 % 3',
        {
            'left': {
                'left': 1,
                'right': 2,
                'operator': '+'
            },
            'right': {
                'left': 5,
                'right': 3,
                'operator': '%'
            },
            'operator': '<<'
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
                        'operator': '+'
                    },
                    'operator': '-'
                },
                'operator': '*'
            },
            'operator': '+'
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
                                    'operator': '+'
                                }
                            ]
                        },
                        'index': {
                            'left': 3,
                            'right': 1,
                            'operator': '-'
                        }
                    },
                    ['identifier', 'second_arg']
                ],
            },
            'right': 1,
            'operator': '**'
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
                                'operator': '+'
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
    ),
    (
        'x = 10',
        {
            'left': ['identifier', 'x'],
            'right': 10,
            'operator': '='
        }
    ),
    (
        'x = y = 1+2',
        {
            'left': ['identifier', 'x'],
            'right': {
                'left': ['identifier', 'y'],
                'right': {
                    'left': 1,
                    'right': 2,
                    'operator': '+'
                },
                'operator': '='
            },
            'operator': '='
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
