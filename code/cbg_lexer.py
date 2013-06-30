#-------------------------------------------------------------------------------
# Lexer for the Cabbage language
#
# Written with PLY
#-------------------------------------------------------------------------------

from __future__ import print_function

from ply import lex

# reserved = {}

tokens = ['NEW',
          'ASSIGN',
          'ID',
          'PRINT',
          'COMPARISON',
          'FLOAT',
          'INTEGER',
          'STRING'] # + list(reserved.values())

literals = (',', '+', '-', '*', '/', '(', ')', '[', ']')

t_NEW = r'\+[ ]*@'
t_ASSIGN = r'<@'
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_PRINT = r'\\@/'
t_COMPARISON = r'\.@|=@|@=|@\.|!@|@'

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
    # turn below into error
    print("Syntax Error: illegal character '{}'".format(t.value[0]))
    t.lexer.skip(1)
    return t

lexer = lex.lex()
