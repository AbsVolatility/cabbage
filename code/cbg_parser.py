#-------------------------------------------------------------------------------
# Parser for the Cabbage language
#
# Written with PLY
#-------------------------------------------------------------------------------

from ply import yacc

from cbg_lexer import tokens
from nodes import *
from cbg_types import *

precedence = [('nonassoc', 'COMPARISON', 'TERNARY'),
              ('left', 'BOOLEAN'),
              ('left', 'BITWISE'),
              ('left', '+', '-'),
              ('right', 'RANGE'),
              ('left', '%'),
              ('left', '*', '/'),
              ('right', '^'),
              ('right', '#', 'FOLD'),
              ('right', 'UNARY'),
              ('left', 'FUNCCALL', 'SLICE')]

def p_s(p):
    's : stmt_list'
    p[0] = Block(p[1])

def p_stmt_list(p):
    '''stmt_list : stmt_
                 | stmt_ stmt_list'''
    p[0] = [p[1]] + (p[2] if len(p)==3 else [])

def p_stmt_(p):
    "stmt_ : stmt ';'"
    p[0] = p[1]

def p_stmt(p):
    '''stmt : assign_stmt
            | augassign_stmt
            | raugassign_stmt
            | index_assign
            | unary_augassign_stmt
            | expression_stmt
            | if_stmt
            | switch_case
            | for_loop
            | while_loop
            | return_stmt
            | break_stmt
            | empty'''
    p[0] = p[1] or NoOp()

def p_assign(p):
    'assign_stmt : ID ASSIGN expression'
    p[0] = Assign(p[1], p[3])

def p_augassign(p):
    'augassign_stmt : ID AUGASSIGN expression'
    p[0] = Assign(p[1], BinaryOp(p[2][:-1], Id(p[1]), p[3]))

def p_raugassign(p):
    'raugassign_stmt : expression RAUGASSIGN ID'
    p[0] = Assign(p[3], BinaryOp(p[2][:-1], p[1], Id(p[3])))

def p_index_assign(p):
    'index_assign : expr_slice ASSIGN expression'
    p[0] = IdxAssign(p[1].lst, p[1].index, p[3])

def p_unary_augassign(p):
    "unary_augassign_stmt : unary_id '<'"
    p[0] = Assign(p[1][0], p[1][1])

def p_unary_id(p):
    '''unary_id : ID
                | UNARY unary_id
                | '+' unary_id %prec UNARY
                | '-' unary_id %prec UNARY
                | '*' unary_id %prec UNARY
                | '|' unary_id %prec UNARY'''
    p[0] = (p[2][0], UnaryOp(p[1], p[2][1])) if len(p)==3 else (p[1], Id(p[1]))

def p_unary_id_type(p):
    "unary_id : '(' TYPE ')' unary_id %prec UNARY"
    p[0] = (p[4][0], UnaryOp(p[2], p[4][1], isfunc=True))

def p_if_stmt(p):
    """if_stmt : if_block
               | if_block '{' stmt_list '}'"""
    p[0] = Ifs(p[1], Block(p[3]) if len(p)==5 else None)

def p_if_block(p):
    """if_block : ':' expression '{' stmt_list '}'
                | ':' expression '{' stmt_list '}' if_block"""
    p[0] = [If(p[2], Block(p[4]))] + (p[6] if len(p)==7 else [])

def p_switch_case(p):
    "switch_case : SWITCH expression cases '{' stmt_list '}'"
    p[0] = switchcase(p[2], p[3], Block(p[5]))

def p_cases(p):
    """cases : ':' expression '{' stmt_list '}'
             | ':' expression '{' stmt_list '}' cases"""
    p[0] = [(p[2], Block(p[4]))] + (p[6] if len(p)==7 else [])

def p_for_loop(p):
    "for_loop : '@' ID ':' expression '{' stmt_list '}'"
    p[0] = For(p[2], p[4], Block(p[6]))

def p_while_loop(p):
    "while_loop : '@' ':' expression '{' stmt_list '}'"
    p[0] = While(p[3], Block(p[5]))

def p_return_stmt(p):
    "return_stmt : '~' expression"
    p[0] = Return(p[2])

def p_break_stmt(p):
    "break_stmt : '~'"
    p[0] = Break()

def p_expression_stmt(p):
    '''expression_stmt : expression'''
    p[0] = Expression(p[1])

def p_expression_bin_op(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression '^' expression
                  | expression '%' expression
                  | expression '#' expression
                  | expression COMPARISON expression
                  | expression BITWISE expression
                  | expression BOOLEAN expression
                  | expression RANGE expression'''
    p[0] = BinaryOp(p[2], p[1], p[3])

def p_expression_unary(p):
    '''expression : UNARY expression
                  | '+' expression %prec UNARY
                  | '-' expression %prec UNARY
                  | '*' expression %prec UNARY
                  | '|' expression %prec UNARY'''
    p[0] = UnaryOp(p[1], p[2])

def p_fold(p):
    '''expression : '+' '/' expression %prec FOLD
                  | '-' '/' expression %prec FOLD
                  | '*' '/' expression %prec FOLD
                  | '/' '/' expression %prec FOLD
                  | '^' '/' expression %prec FOLD
                  | '%' '/' expression %prec FOLD
                  | BITWISE '/' expression %prec FOLD
                  | BOOLEAN '/' expression %prec FOLD'''
    p[0] = Fold(p[1], p[3])

def p_expression_type_conv(p):
    "expression : '(' TYPE ')' expression %prec UNARY"
    p[0] = UnaryOp(p[2], p[4], isfunc=True)

def p_expression_ternary(p):
    "expression : expression '?' expression ':' expression %prec TERNARY"
    p[0] = Ternary(p[1], p[3], p[5])

def p_expression_slce(p):
    'expression : expr_slice'
    p[0] = p[1]

def p_expression_slice(p):
    '''expr_slice : expression '[' expression ']' %prec SLICE
                  | expression '[' slice ']' %prec SLICE'''
    p[0] = Slice(p[1], p[3])

def p_slice(p):
    '''slice : op_expr ':' op_expr
             | op_expr ':' op_expr ':' op_expr'''
    p[0] = Slce(p[1], p[3] if len(p)>=4 else none, p[5] if len(p)==6 else none)

def p_op_expr(p):
    '''op_expr : empty
               | expression'''
    p[0] = p[1] or none

def p_expression_parens(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_func_call(p):
    "expression : TYPE '(' expression_list ')'"
    p[0] = FunctionCall(Id(p[1], special=True), ParamList(p[3]))

def p_func_call_lit(p):
    "expression : expression '(' expression_list ')' %prec FUNCCALL"
    p[0] = FunctionCall(p[1], ParamList(p[3]))

def p_expression_literal(p):
    'expression : literal'
    p[0] = p[1]

def p_expression_id(p):
    'expression : ID'
    p[0] = Id(p[1])

def p_expression_special_id(p):
    'expression : SPECIAL_ID'
    p[0] = Id({'@<': 'input', '@>': 'print'}[p[1]], special=True)

def p_expression_list(p):
    '''expression_list : empty
                       | expression
                       | expression ',' expression_list'''
    p[0] = ([p[1]] + p[3]) if len(p)==4 else ([p[1]] if p[1] else [])

def p_lambda_def(p):
    """literal : '{' id_list ':' expression '}'
               | '{' empty ':' expression '}'"""
    p[0] = LambdaDef(p[2] or [], p[4])

def p_func_def(p):
    """stmt : FUNCDEF ID ':' id_list '{' stmt_list '}'
            | FUNCDEF ID ':' empty '{' stmt_list '}'"""
    p[0] = FunctionDef(p[2], p[4] or [], Block(p[6]))

def p_id_list(p):
    '''id_list : ID
               | ID id_list'''
    p[0] = [p[1]] + (p[2] if len(p)==4 else [])

def p_literal_integer(p):
    'literal : INTEGER'
    p[0] = cbgInteger(p[1])

def p_literal_float(p):
    'literal : FLOAT'
    p[0] = cbgFloat(p[1])

def p_literal_string(p):
    '''literal : STRING
               | RAWSTRING'''
    p[0] = cbgString(p[1])

def p_literal_bool(p):
    'literal : BOOL'
    p[0] = true if p[1] else false

def p_literal_none(p):
    'literal : NONE'
    p[0] = none

def p_literal_other(p):
    '''literal : list
               | set'''
    p[0] = p[1]

def p_list(p):
    "list : '[' expression_list ']'"
    p[0] = cbgList(p[2])

def p_set(p):
    "set : '{' expression_list '}'"
    p[0] = cbgSet(p[2])

def p_list_comp(p):
    """list : '[' expression '|' asgn_list ']'
            | '[' expression '|' asgn_list ':' expression ']'"""
    p[0] = ListComp(p[2], p[4], p[6] if len(p)==8 else None)

def p_asgn_list(p):
    '''asgn_list : assign_stmt
                 | assign_stmt ',' asgn_list'''
    p[0] = [p[1]] + (p[3] if len(p)==4 else [])

def p_empty(p):
    'empty :'

def p_error(p):
    raise SyntaxError('invalid syntax')

parser = yacc.yacc()