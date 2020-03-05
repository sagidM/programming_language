from typing import List
from .helpers.text_window import TextWindow

class Lexer:
    def __init__(self, code):
        self.text_window = TextWindow(code)
    
    def lex(self) -> List[str]:
        tokens = []
        text_window = self.text_window
        while text_window.may_continue():
            ch = text_window.peek_char()
            start = text_window.offset
            
            token_type = self.scan_positive_number()
            if token_type:
                pass
            elif ch in '*/&|' and text_window.peek_char(1) == ch:
                token_type = ch + ch
                text_window.advance_char(2)
            elif ch in '+-*%=^;()':
                token_type = ch
                text_window.advance_char()
            elif ch == ' ':
                text_window.advance_char()
                continue
            else:
                raise SyntaxError(f'Unknown token at :{text_window.offset} "{ch}"')
            token_value = text_window.text[start:text_window.offset]
            tokens.append((token_type, token_value))
        tokens.append(('TERMINATE_TOKEN', ''))
        return tokens

    # 2, 5.2, -3, -5.3, .7, -.6, 6., -6.,
    # 5e1, -5e1, 5.1e1, -5.1e1, .1e1, -.1e1, 1e1, 1e-1
    # {f}e-?{i}
    def scan_positive_number(self):
        text_window = self.text_window
        float_result = self.scan_positive_float()
        if not float_result:
            return None
        if in_no_except(text_window.peek_char(), 'eE'):
            text_window.advance_char()
            if in_no_except(text_window.peek_char(), '+-'):
                text_window.advance_char()
            if not self.scan_positive_int():
                raise SyntaxError('An int value was not found after the exponent sign E')
            return 'exponent_value'
        return float_result

    # {i}, {i}.{i}, {i}., .{i}
    def scan_positive_float(self):
        start = self.text_window.offset
        self.scan_positive_int()
        if self.text_window.peek_char() == '.':
            self.text_window.advance_char()
            self.scan_positive_int()
            return 'float_value' if start < self.text_window.offset else None
        return 'int_value' if start < self.text_window.offset else None

    def scan_positive_int(self):
        ch = self.text_window.peek_char()
        start = self.text_window.offset
        while self.text_window.may_continue() and ch.isdigit():
            self.text_window.advance_char()
            ch = self.text_window.peek_char()
        return start < self.text_window.offset

def in_no_except(value, seq):
    return value is not None and value in seq
def is_number_token(token):
    return token[0] in ('float_value', 'int_value', 'exponent_value')