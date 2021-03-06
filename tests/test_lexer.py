import unittest
from src.lexer import Lexer

one_line_params = (
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
        '\n-\r\n+',
        [
            # CRLF is not supported, only LF,
            # thus '\n' is the type of the token '\r\n'
            ('\n', '\n'), ('-', '-'), ('\n', '\r\n'), ('+', '+')
        ]
    ),
    (
        '43 + -123 && -4.5 ** 5',
        [
            ('int_value', '43'), ('+', '+'), ('-', '-'), ('int_value', '123'),
            ('&&', '&&'), ('-', '-'), ('float_value', '4.5'), ('**', '**'), ('int_value', '5')
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
    ),
    (
        '5 + x - another_variable + y',
        [
            ('int_value', '5'), ('+', '+'), ('identifier', 'x'), ('-', '-'),
            ('identifier', 'another_variable'), ('+', '+'), ('identifier', 'y')
        ]
    ),
    (
        'x = 10',
        [('identifier', 'x'), ('=', '='), ('int_value', '10')]
    ),
    # Keywords
    (
        'let not_implemented = 1',
        [('let', 'let'), ('identifier', 'not_implemented'), ('=', '='), ('int_value', '1')]
    ),
    (
        'if 1 < 2',
        [('if', 'if'), ('int_value', '1'), ('<', '<'), ('int_value', '2')]
    ),
)


multiline_params = (
    (
'''
1 + 2.5
  4
   3 + 6
'''.strip('\n'),
        [
            ('int_value', '1'), ('+', '+'), ('float_value', '2.5'), ('\n', '\n'),
            ('indentation', '  '), ('int_value', '4'), ('\n', '\n'),
            ('indentation', '   '), ('int_value', '3'), ('+', '+'), ('int_value', '6')
        ]
    ),
)


class TestLexerMethods(unittest.TestCase):
    def _test_with_params(self, params):
        for i in range(len(params)):
            expr, lex_expected = params[i]
            lex_actual = Lexer(expr).lex()
            # Every lexer result ends with this token. It is nicer and
            # more performant to remove it from the result instead of
            # mutating data or creating new lex_expected (using + on arrays)
            self.assertEqual(('TERMINATE_TOKEN', ''), lex_actual.pop())
            self.assertEqual(lex_expected, lex_actual,
                f'Error on the {i} param set with the expression "{expr}"')

    def test_one_line(self):
        self._test_with_params(one_line_params)
    def test_multiline(self):
        self._test_with_params(multiline_params)

if __name__ == '__main__':
    unittest.main()
