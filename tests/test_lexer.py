import unittest
from src.lexer import Lexer

expression_params = (
    (
        '0 1 222 3.12 44. .55 6e0 7e-3 8.2e1 9.e2 10.e-0 .11e1 .12e-2 13.11e-1',
        [
            ('int_value', '0'), ('int_value', '1'), ('int_value', '222'),
            ('float_value', '3.12'), ('float_value', '44.'), ('float_value', '.55'),
            ('exponent_value', '6e0'), ('exponent_value', '7e-3'),
            ('exponent_value', '8.2e1'), ('exponent_value', '9.e2'),
            ('exponent_value', '10.e-0'), ('exponent_value', '.11e1'),
            ('exponent_value', '.12e-2'), ('exponent_value', '13.11e-1'),
        ]
    ),
    (
        '43 + -123 && -4.5',
        [
            ('int_value', '43'), ('+', '+'), ('-', '-'), ('int_value', '123'),
            ('&&', '&&'), ('-', '-'), ('float_value', '4.5')
        ],
    ),
    (
        '-.6    - 2. * -7. // 0',
        [
            ('-', '-'), ('float_value', '.6'), ('-', '-'), ('float_value', '2.'),
            ('*', '*'), ('-', '-'), ('float_value', '7.'), ('//', '//'), ('int_value', '0')
        ]
    ),
    (
        '4**1',
        [
            ('int_value', '4'), ('**', '**'), ('int_value', '1')
        ]
    )
)

class TestLexerMethods(unittest.TestCase):
    def test_expressions(self):
        for i in range(len(expression_params)):
            expr, lex_expected = expression_params[i]
            lex_actual = Lexer(expr).lex()
            # Every lexer result ends with this token. It is nicer and
            # more permormant to remove it from the result instead of
            # mutating data or creating new lex_expected (using + on arrays)
            self.assertEqual(('TERMINATE_TOKEN', ''), lex_actual.pop())
            self.assertEqual(lex_expected, lex_actual,
                f'Error on the {i} param set with the expression "{expr}"')


if __name__ == '__main__':
    unittest.main()