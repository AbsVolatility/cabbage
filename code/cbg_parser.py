#-------------------------------------------------------------------------------
# Parser for the Cabbage language
#
# Written with PLY
#-------------------------------------------------------------------------------

from __future__ import print_function

from ply import yacc

from cbg_lexer import tokens
from nodes import *
from cbg_types import *

precedence = [('nonassoc', 'COMPARISON'),
              ('left', '+', '-'),
              ('left', '*', '/')]

def p_stmt(p):
    '''stmt : new_stmt
            | print_stmt
            | assign_stmt
            | func_call
            | expression_stmt'''
    p[0] = p[1]

def p_new(p):
    '''new_stmt : NEW ID
                | NEW ID ASSIGN expression'''
    p[0] = New(p[2], p[4] if len(p)==5 else None)

def p_print(p):
    '''print_stmt : PRINT
                  | PRINT expression'''
    p[0] = Print(p[2] if len(p)==3 else cbgString(''))

def p_assign(p):
    'assign_stmt : ID ASSIGN expression'
    p[0] = Assign(p[1], p[3])

def p_func_call(p):
    "func_call : ID '(' expression_list ')'"
    p[0] = Function(p[1], cbgList(p[3]))

def p_expression_stmt(p):
    'expression_stmt : expression'
    p[0] = Expression(p[1])

def p_expression_bin_op(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression COMPARISON expression'''
    p[0] = BinaryOp(p[2], p[1], p[3])

def p_expression_parens(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_expression_literal(p):
    'expression : literal'
    p[0] = p[1]

def p_expression_id(p):
    'expression : ID'
    p[0] = Id(p[1])

def p_expression_list(p):
    '''expression_list : empty
                       | expression
                       | expression ',' expression_list'''
    p[0] = ([p[1]] + p[3]) if len(p)==4 else ([p[1]] if p[1] else [])

def p_literal_integer(p):
    'literal : INTEGER'
    p[0] = cbgInteger(p[1])

def p_literal_float(p):
    'literal : FLOAT'
    p[0] = cbgFloat(p[1])

def p_literal_string(p):
    'literal : STRING'
    p[0] = cbgString(p[1])

def p_literal_list(p):
    'literal : list'
    p[0] = p[1]

def p_list(p):
    "list : '[' expression_list ']'"
    p[0] = cbgList(p[2])

def p_empty(p):
    'empty :'

def p_error(p):
    print('Syntax Error')

parser = yacc.yacc()
