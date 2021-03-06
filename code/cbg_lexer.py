#-------------------------------------------------------------------------------
# Lexer for the Cabbage language
#
# Hand-written
# Supports 2.7, 3.0+
#-------------------------------------------------------------------------------
# Rules:
# - ID + reserved  [a-zA-Z_][a-zA-Z0-9_]*
# - SPECIAL_ID     @[<>]
# - INTEGER        [0-9]+
# - FLOAT          [0-9]+\.[0-9]+
# - STRING         '.*?'
# - ASSIGN         <-
# - FUNCDEF        \+@
# - SWITCH         -:
# - COMPARISON     <|<=|!=|>|>=|=
# - AUGASSIGN      (\+|-|\*|/|%|\.(&|\||\^))<
# - RAUGASSIGN     (\+|-|\*|/|%|\.(&|\||\^))>
# - BITWISE        \.(&|\||\^)
# - RANGE          \.\.
# - UNARY          \.~|!|`
# - BOOLEAN        &&|\|\|
# - literals       +-*/^%.|,()[]:{}?@~#;
#-------------------------------------------------------------------------------

import ast

# `tokens` is required for use with the PLY parser module
tokens = ['ASSIGN', 'AUGASSIGN', 'RAUGASSIGN',
          'FUNCDEF',
          'SWITCH',
          'BITWISE', 'BOOLEAN',
          'UNARY',
          'RANGE',
          'COMPARISON',
          'ID', 'SPECIAL_ID',
          'FLOAT', 'INTEGER', 'RAWSTRING', 'STRING'] + ['BOOL', 'NONE', 'TYPE']

class Token:
    def __init__(self, value, name, pos, lineno):
        self.value = value
        self.type = name
        self.lexpos = pos
        self.lineno = lineno
    def __repr__(self):
        return 'Token({!r}, {}, {}, {})'.format(self.value, self.type, self.lexpos, self.lineno)

class Lexer:
    def __init__(self):
        self.input('')
        self.reserved = {'true': 'BOOL', 'false': 'BOOL',
                         'none': 'NONE',
                         'int': 'TYPE', 'float': 'TYPE',
                         'str': 'TYPE', 'list': 'TYPE', 'tuple': 'TYPE', 'set': 'TYPE',
                         'func': 'TYPE',
                         'bool': 'TYPE'}
    def input(self, input_str):
        self.input_str = input_str
        self.pointer = -1
        self.lineno = 1
    def next(self):
        self.pointer += 1
        return self.input_str[self.pointer : self.pointer + 1]
    def push(self):
        self.pointer -= 1
    def options(self, chars, token, pos, lineno):
        c = self.next()
        for k, v in chars.items():
            if c == k:
                return token + c, v, pos, lineno
        self.push()
    def token(self):
        while True:
            c = self.next()
            if c == '\n':
                self.lineno += 1
            elif c != ' ':
                break
        if not c:
            return None
        pos, lineno = self.pointer, self.lineno
        if c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
            token = c
            while True:
                c = self.next()
                if not (c and c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'):
                    self.push()
                    break
                token += c
            name = self.reserved.get(token, 'ID')
            if name != 'ID':
                token = {'true': True, 'false': False, 'none': None}.get(token, token)
            return Token(token, name, pos, lineno)
        elif c in '0123456789':
            token = c
            while True:
                c = self.next()
                if not (c and c in '0123456789'):
                    self.push()
                    break
                token += c
            if self.next() == '.':
                token += '.'
                c = self.next()
                if not (c and c in '0123456789'):
                    self.push()
                    token = token[:-1]
                else:
                    token += c
                    while True:
                        c = self.next()
                        if not (c and c in '0123456789'):
                            self.push()
                            return Token(float(token), 'FLOAT', pos, lineno)
                        token += c
            self.push()
            return Token(int(token), 'INTEGER', pos, lineno)
        elif c == "'":
            token = ''
            while True:
                c = self.next()
                if not c:
                    raise SyntaxError('unexpected EOL while parsing')
                if c == "'":
                    return Token(token, 'RAWSTRING', pos, lineno)
                token += c
        elif c == '"':
            token = '"'
            while True:
                c = self.next()
                if not c:
                    raise SyntaxError('unexpected EOL while parsing')
                if c == '"':
                    if token[-1] == '\\':
                        pass
                    else:
                        token += '"'
                        return Token(ast.literal_eval(token), 'STRING', pos, lineno)
                token += c
        elif c == '&':
            if self.next() == '&':
                return Token('&&', 'BOOLEAN', pos, lineno)
            raise SyntaxError("illegal character {!r} at position {}".format(c, self.pointer))
        elif c == '.':
            token = c
            c = self.next()
            if c and c in '&|^':
                token += c
                match = self.options({'<': 'AUGASSIGN', '>': 'RAUGASSIGN'}, token, pos, lineno)
                if match:
                    return Token(*match)
                return Token(token, 'BITWISE', pos, lineno)
            self.push()
            match = self.options({'.':  'RANGE', '~': 'UNARY'}, token, pos, lineno)
            if match:
                return Token(*match)
            raise SyntaxError("illegal character {!r} at position {}".format(c, self.pointer))
        elif c == '<':
            match = self.options({'-': 'ASSIGN', '=': 'COMPARISON'}, c, pos, lineno)
            if match:
                return Token(*match)
            return Token('<', 'COMPARISON', pos, lineno)
        elif c in '*/^%':
            match = self.options({'<': 'AUGASSIGN', '>': 'RAUGASSIGN'}, c, pos, lineno)
            if match:
                return Token(*match)
            return Token(c, c, pos, lineno)
        elif c == '+':
            match = self.options({'<': 'AUGASSIGN', '>': 'RAUGASSIGN', '@': 'FUNCDEF'}, c, pos, lineno)
            if match:
                return Token(*match)
            return Token('+', '+', pos, lineno)
        elif c == '-':
            match = self.options({'<': 'AUGASSIGN', '>': 'RAUGASSIGN', ':': 'SWITCH'}, c, pos, lineno)
            if match:
                return Token(*match)
            return Token('-', '-', pos, lineno)
        elif c == '@':
            match = self.options({'<': 'SPECIAL_ID', '>': 'SPECIAL_ID'}, c, pos, lineno)
            if match:
                return Token(*match)
            return Token('@', '@', pos, lineno)
        elif c == '!':
            if self.next() == '=':
                return Token('!=', 'COMPARISON', pos, lineno)
            self.push()
            return Token('!', 'UNARY', pos, lineno)
        elif c == '>':
            if self.next() == '=':
                return Token('>=', 'COMPARISON', pos, lineno)
            self.push()
            return Token('>', 'COMPARISON', pos, lineno)
        elif c == '|':
            if self.next() == '|':
                return Token('||', 'BOOLEAN', pos, lineno)
            self.push()
            return Token('|', '|', pos, lineno)
        elif c == '`':
            return Token(c, 'UNARY', pos, lineno)
        elif c == '=':
            return Token(c, 'COMPARISON', pos, lineno)
        elif c in ',()[]:{}?~#;':
            return Token(c, c, pos, lineno)
        raise SyntaxError("illegal character {!r} at position {}".format(c, self.pointer))
    def run(self):
        l = []
        while True:
            next_token = self.token()
            if next_token is None:
                return l
            l.append(next_token)

lexer = Lexer()