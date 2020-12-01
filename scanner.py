from typing import List

from token import Token, TokenType

class Scanner:
    tokens: List
    start = 0
    current = 0
    line = 1
    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }
    def __init__(self,source,on_error=print):
        self.source = source
        self.tokens = []
        self.on_error = on_error

    def is_at_end(self):
        return self.current >= len(self.source)

    def get_tokens(self):
        while(not self.is_at_end()):
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF,"",None,self.line))
        return self.tokens

    def scan_token(self):
        c = self._advance()
        token_options = {
            "(": lambda: self._add_token(TokenType.LEFT_PAREN),
            ")": lambda: self._add_token(TokenType.RIGHT_PAREN),
            "{": lambda: self._add_token(TokenType.LEFT_BRACE),
            "}": lambda: self._add_token(TokenType.RIGHT_BRACE),
            ",": lambda: self._add_token(TokenType.COMMA),
            ".": lambda: self._add_token(TokenType.DOT),
            "-": lambda: self._add_token(TokenType.MINUS),
            "+": lambda: self._add_token(TokenType.PLUS),
            ";": lambda: self._add_token(TokenType.SEMICOLON),
            "*": lambda: self._add_token(TokenType.STAR),
            "!": lambda: self._add_token(
                TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG
            ),
            "=": lambda: self._add_token(
                TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL
            ),
            "<": lambda: self._add_token(
                TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
            ),
            ">": lambda: self._add_token(
                TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
            ),
            "/": self._operator_slash,
            " ": type(None),
            "\r": type(None),
            "\t": type(None),
            "\n": self._operator_newline,
            '"': self._string,
        }
        try:
            option = token_options[c]
            option()
        except KeyError:
            if c.isdigit():
                self._number()
            elif c.isalpha() or c == "_":
                self._identifier()
            elif self.on_error:
                self.on_error(self.line, f"Unexpected character: {c}")
            else:
                raise
    def _operator_newline(self):
        self.line += 1

    def _peek_next(self):
        if(self.current + 1 >= len(self.source)):
            return '\0'
        return self.source[self.current+1]

    def _identifier(self):
        while self._peek().isalnum() or self._peek() == "_":
            self._advance()
        token_type = self.keywords.get(self.source[self.start:self.current],TokenType.IDENTIFIER)
        self._add_token(token_type)
    def _number(self):
        while self._peek().isdigit():
            self._advance()
        if(self._peek() == '.' and self._peek_next().isdigit()):
            self._advance()
            while self._peek().isdigit():
                self._advance()
        self._add_token(TokenType.NUMBER,float(self.source[self.start:self.current]))

    def _string(self):
        while(self._peek() != '"' and not self.is_at_end()):
            if self._peek() == "\n":
                self.line += 1
            self._advance()
        if self.is_at_end():
            self.on_error(f"Unterminated String on line {self.line}")
            return
        self._advance()
        value = self.source[self.start + 1 : self.current - 1]
        self._add_token(TokenType.STRING,value)

    def _advance(self):
        self.current += 1
        return self.source[self.current-1]

    def _add_token(self,token_type,literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type,text,literal,self.line))

    def _match(self, expected: str):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def _operator_slash(self):
        if(self._match('/')):
            while(self._peek() != '\n' and not self.is_at_end()):
                self._advance()
        else:
            self._add_token(TokenType.SLASH)

    def _peek(self):
        if(self.is_at_end()):
            return '\0'
        return self.source[self.current]