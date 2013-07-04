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
from cbg_errors import CbgSyntaxError

precedence = [('nonassoc', 'COMPARISON', 'TERNARY'),
              ('left', 'BOOLEAN'),
              ('left', 'BITWISE'),
              ('left', '+', '-'),
              ('nonassoc', 'RANGE'),
              ('left', '%'),
              ('left', '*', '/'),
              ('right', '^'),
              ('left', 'SLICE'),
              ('right', 'UNARY')]

def p_s(p):
    's : stmt_list'
    p[0] = Block(p[1])

def p_stmt_list(p):
    '''stmt_list : empty
                 | stmt_ stmt_list'''
    p[0] = ([p[1]] + p[2]) if len(p)==3 else []

def p_stmt_(p):
    "stmt_ : stmt ';'"
    p[0] = p[1]

def p_stmt(p):
    '''stmt : print_stmt
            | assign_stmt
            | expression_stmt
            | if_stmt
            | for_loop
            | while_loop
            | return_stmt
            | break_stmt'''
    p[0] = p[1]

def p_print(p):
    '''print_stmt : PRINT
                  | PRINT expression'''
    p[0] = Print(p[2] if len(p)==3 else cbgString(''))

def p_assign(p):
    'assign_stmt : ID ASSIGN expression'
    p[0] = Assign(p[1], p[3])

def p_if_stmt(p):
    """if_stmt : if_block
               | if_block '{' stmt_list '}'"""
    p[0] = Ifs(p[1], Block(p[3]) if len(p)==5 else None)

def p_if_block(p):
    """if_block : ':' expression '{' stmt_list '}'
                | ':' expression '{' stmt_list '}' if_block"""
    p[0] = [If(p[2], Block(p[4]))] + (p[6] if len(p)==7 else [])

def p_for_loop(p):
    "for_loop : '@' ID ':' expression '{' stmt_list '}'"
    p[0] = For(p[2], p[4], Block(p[6]))

def p_while_loop(p):
    "while_loop : '@' expression '{' stmt_list '}'"
    p[0] = While(p[2], Block(p[4]))

def p_return_stmt(p):
    "return_stmt : '~' expression"
    p[0] = Return(p[2])

def p_break_stmt(p):
    "break_stmt : '~'"
    p[0] = Break()

def p_expression_stmt(p):
    'expression_stmt : expression'
    p[0] = Expression(p[1])

def p_expression_bin_op(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression '^' expression
                  | expression '%' expression
                  | expression COMPARISON expression
                  | expression BITWISE expression
                  | expression BOOLEAN expression
                  | expression RANGE expression'''
    p[0] = BinaryOp(p[2], p[1], p[3])

def p_expression_unary(p):
    '''expression : UNARY expression
                  | '+' expression
                  | '-' expression'''
    p[0] = UnaryOp(p[1], p[2])

def p_expression_ternary(p):
    "expression : expression '?' expression ':' expression %prec TERNARY"
    p[0] = Ternary(p[1], p[3], p[5])

def p_expression_slice(p):
    '''expression : expression '[' expression ']' %prec SLICE
                  | expression '[' slice ']' %prec SLICE'''
    p[0] = Slice(p[1], p[3])

def p_slice(p):
    '''slice : op_expr ':' op_expr
             | op_expr ':' op_expr ':' op_expr'''
    p[0] = Slce(p[1], p[3] if len(p)>=4 else cbgNone(), p[5] if len(p)==6 else cbgNone())

def p_op_expr(p):
    '''op_expr : empty
               | expression'''
    p[0] = p[1]

def p_expression_parens(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_func_call(p):
    "expression : ID '(' expression_list ')'"
    p[0] = FunctionCall(Id(p[1]), ParamList(p[3]))

def p_func_call_lit(p):
    "expression : literal '(' expression_list ')'"
    p[0] = FunctionCall(p[1], ParamList(p[3]))

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

def p_func_def(p):
    "literal : '{' id_list ':' stmt_list '}'"
    p[0] = FunctionDef(p[2], Block(p[4]))

def p_id_list(p):
    '''id_list : empty
               | ID
               | ID ',' id_list'''
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

def p_literal_bool(p):
    '''literal : TRUE
               | FALSE'''
    p[0] = cbgBool(p[1])

def p_literal_none(p):
    'literal : NONE'
    p[0] = cbgNone()

def p_literal_other(p):
    'literal : list'
    p[0] = p[1]

def p_list(p):
    "list : '[' expression_list ']'"
    p[0] = cbgList(p[2])

def p_empty(p):
    'empty :'
    p[0] = cbgNone()

def p_error(p):
    raise CbgSyntaxError('invalid syntax')

parser = yacc.yacc()
