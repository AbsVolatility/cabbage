#-------------------------------------------------------------------------------
# Master lexer for the Cabbage language
#
# Written with PLY
#-------------------------------------------------------------------------------

from ply import lex

# support_reserved = {}

# rebel_reserved = {}

# reserved = list(support_reserved.values()) + list(rebel_reserved.values())

tokens = ['NEW',
          'ASSIGN',
          'ID',
          'PRINT',
          'INTEGER',
          'FLOAT',
          'STRING',
          'COMPARISON'] # + reserved

literals = (',', '+', '-', '*', '/', '(', ')', '[', ']')

states = [('full', 'inclusive'),
          ('support', 'inclusive'),
          ('rebel', 'inclusive')]

#-------------------------------------------------------------------------------
# common tokens

def t_INTEGER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r"'.*'"
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

#-------------------------------------------------------------------------------
# other tokens

t_full_PRINT = r'\\@/'
t_support_PRINT = r'plant'

t_full_NEW = r'\+[ ]*@'
t_support_NEW = r'new[ ]+cabbage'
t_rebel_NEW = r'var'

t_full_COMPARISON = r'\.@|=@|@=|@\.|@'
t_support_rebel_COMPARISON = r'<=|>=|<|=|>'

t_support_full_ASSIGN = r'<@'
t_rebel_ASSIGN = r'<-'

t_full_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_support_ID = r'(cabbage|cbg)[a-zA-Z0-9_]+'

def t_rebel_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # t.type = rebel_reserved.get(t.value, 'ID')
    if t.value == 'print':
        t.type = 'PRINT'
    return t

def t_support_full_FLOAT(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

lexer = lex.lex()
lexer.begin('full')
