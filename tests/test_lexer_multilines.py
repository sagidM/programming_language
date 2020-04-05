import unittest
# unittest finds this import and runs its methods
from test_lexer import TestLexerMethods


expression_params = (
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


if __name__ == '__main__':
    unittest.main()