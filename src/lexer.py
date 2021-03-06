import re
from typing import List
from .helpers.text_window import TextWindow


identifier_regex = re.compile(r'[^\W\d]\w*')

# TODO: build trie
reserved_tokens = '\n\
 + - * / % = ^ ~ & | < > ; , . ( ) [ ]\
 ** // && || << >>\
 <=>'.split(' ')
reserved_keywords = 'let if while for'.split(' ')
# TODO: get rid of this when create the Trie to scan reserved_tokens
reserved_tokens.sort(key=lambda s: len(s), reverse=True)

class Lexer:
    def __init__(self, code):
        self.text_window = TextWindow(code)

    def lex(self) -> List[str]:
        tokens = []
        text_window = self.text_window
        save_indentation = True     # save indentation from the beginning of every new line
        while text_window.may_continue():
            ch = text_window.peek_char()
            start = text_window.offset

            token_type = self.scan_positive_number()
            if token_type:
                pass
            elif save_indentation and self.scan_indentation():
                token_type = 'indentation'
            elif ch == ' ':
                text_window.advance_char()
                continue
            elif self.scan_fixed_token('\r\n'):
                token_type = '\n'  # does not support CRLF, only LF
            elif self.scan_fixed_tokens(reserved_tokens):
                token_type = text_window.text[start:text_window.offset]
            elif self.scan_identifier():
                # TODO: avoid the doule slicing here and below not inflating the code
                token_value = text_window.text[start:text_window.offset]
                token_type = token_value if token_value in reserved_keywords else 'identifier'
            else:
                raise SyntaxError(f'Unknown token at :{text_window.offset} "{ch}"')
            save_indentation = token_type == '\n'
            token_value = text_window.text[start:text_window.offset]
            tokens.append((token_type, token_value))
        tokens.append(('TERMINATE_TOKEN', ''))
        return tokens

    def scan_identifier(self):
        text_window = self.text_window
        res = identifier_regex.search(text_window.text, text_window.offset)
        if res is None or res.start() != text_window.offset:
            return False
        text_window.advance_char(len(res.group(0)))
        return True

    def scan_fixed_tokens(self, tokens):
        for token in tokens:
            if self.scan_fixed_token(token):
                return True
        return False

    def scan_fixed_token(self, token):
        for i in range(len(token)):
            if token[i] != self.text_window.peek_char(i):
                return False
        self.text_window.advance_char(len(token))
        return True

    def scan_indentation(self):
        text_window = self.text_window
        INDENTS = ' \t'
        has_indent = False
        while text_window.may_continue() and text_window.text[text_window.offset] in INDENTS:
            text_window.advance_char()
            has_indent = True
        return has_indent

    # 2, 5.2, -3, -5.3, .7, -.6, 6., -6.,
    # 5e1, -5e1, 5.1e1, -5.1e1, .1e1, -.1e1, 1e1, 1e-1
    # i, f, {f}e-?{i}
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
        if self.scan_positive_int() and self.text_window.peek_char() == '.' or\
           self.text_window.peek_char() == '.' and (self.text_window.peek_char(1) or '').isdigit():
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
