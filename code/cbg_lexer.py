#-------------------------------------------------------------------------------
# Lexer for the Cabbage language
#
# Written with PLY
#-------------------------------------------------------------------------------

from __future__ import print_function

from ply import lex
from cbg_errors import CbgSyntaxError

reserved = {'True': 'TRUE',
            'False': 'FALSE',
            'None': 'NONE'}

tokens = ['ASSIGN',
          'PRINT',
          'BITWISE',
          'BOOLEAN',
          'UNARY',
          'RANGE',
          'COMPARISON',
          'ID',
          'FLOAT',
          'INTEGER',
          'STRING'] + list(reserved.values())

literals = (',', '+', '-', '*', '/', '^', '%', '(', ')', '[', ']', ':', '{', '}', '?', ';', '@', '~')

t_ASSIGN = r'<-'
t_PRINT = r'\\@/'
t_BITWISE = r'\.(&|\||^)'
t_BOOLEAN = r'&|\|'
t_UNARY = r'\.~|!(?!=)'
t_RANGE = r'\.\.'
t_COMPARISON = r'<=|>=|<(?!-)|>|=|!='

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    if t.type != 'ID':
        t.value = {'True': True,
                   'False': False,
                   'None': None}[t.value]
    return t

def t_FLOAT(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r"'.*?'"
    t.value = t.value[1:-1]
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' '

def t_error(t):
    raise CbgSyntaxError("illegal character '{}'".format(t.value[0]))

lexer = lex.lex()
