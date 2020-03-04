from lexer import Lexer

result = Lexer('43 + 123 && 4.5').lex()
print(result)