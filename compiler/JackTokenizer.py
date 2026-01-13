import re
from Constants import *

class JackTokenizer:
    def __init__(self, file):
        with open(file, 'r') as f:
            self.content = f.read()
        
        self.current_token = None
        self.token_index = -1
        self.tokens = self._tokenize(self.content)

    def _tokenize(self, content):
        comment_pattern = r'//.*|/\*[\s\S]*?\*/'
        content_no_comments = re.sub(comment_pattern, '', content)
        symbol_pattern = r'[{}()\[\].,;+\-*/&|<>=~]'
        int_pattern = r'\d+'
        string_pattern = r'"[^"\n]*"'  
        identifier_pattern = r'[a-zA-Z_]\w*'

        
        token_pattern = re.compile(f'{string_pattern}|{symbol_pattern}|{int_pattern}|{identifier_pattern}')
        
        return token_pattern.findall(content_no_comments)    

    def has_more_tokens(self):
        return self.token_index < len(self.tokens) - 1

    def advance(self):
        self.token_index += 1
        self.current_token = self.tokens[self.token_index]

    def token_type(self):
        token = self.current_token
        if token in KEYWORDS:
            return KEYWORD
        if token in SYMBOLS:
            return SYMBOL
        if token.isdigit():
            return INT_CONST
        if token.startswith('"'):
            return STRING_CONST
        return IDENTIFIER

    def keyword(self):
        return self.current_token

    def symbol(self):
        return self.current_token

    def identifier(self):
        return self.current_token

    def int_val(self):
        return int(self.current_token)

    def string_val(self):
        return self.current_token[1:-1]