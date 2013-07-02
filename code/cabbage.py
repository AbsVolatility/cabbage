#-------------------------------------------------------------------------------
# Code generator and executer for the Cabbage language
#-------------------------------------------------------------------------------

from __future__ import print_function
import copy

from cbg_lexer import lexer
from cbg_parser import parser

from cbg_builtins import *
from cbg_operators import *
from cbg_types import *

namespace = {'__builtins__': {'print': print,
                              'cbgInteger': cbgInteger,
                              'cbgFloat': cbgFloat,
                              'cbgString': cbgString,
                              'cbgList': cbgList,
                              'cbgBool': cbgBool,
                              'cbgNone': cbgNone},
             'base': base,
             'input': input}

def indent(lst):
    return ['    ' + i for i in lst]  # indent by 4 spaces

def gen(node, print_expr=False):
    node_type = node.type
    if node_type == 'new':
        name = node.name
        if name == '__builtins__':
            print("Can't assign to '__builtins__'")  # turn into error
            return ''
        elif name in namespace:
            print("Can't reinitialize a variable")  # turn into error
            return ''
        else:
            return '{} = {!r}'.format(name, gen(node.value))
    elif node_type == 'print':
        return "print({})".format(gen(node.value))
    elif node_type == 'assign':
        name = node.name
        if name not in namespace:
            print('Unknown cabbage')  # turn into error
            return ''
        elif name == '__builtins__':
            print("Can't assign to '__builtins__'")  # turn into error
            return ''
        else:
            return '{} = {!r}'.format(name, gen(node.value))
    elif node_type == 'id':
        return eval(node.name, namespace)
    elif node_type == 'expression':
        return 'print("{}")'.format(gen(node.value)) if print_expr else 'pass'
    elif node_type == 'binary_op':
        return eval('{}({!r}, {!r})'.format(node.op, gen(node.arg1), gen(node.arg2)), globals())
    elif node_type == 'unary_op':
        return eval('{}({!r})'.format(node.op, gen(node.arg)), globals())
    elif node_type == 'function':
        return '{}(*{})'.format(node.name, gen(node.param_list))
    elif node_type == 'if':
        code = ['if {}:'.format(gen(node.cond))] + indent(gen(node.if_block))
        if node.else_block is not None:
            code += ['else:'] + indent(gen(node.else_block))
        return code
    elif node_type == 'ternary':
        return eval('({}) if ({}) else ({})'.format(gen(node.if_block), gen(node.cond), gen(node.else_block)))
    elif node_type == 'block':
        return [gen(i) for i in node.code]
    else:  # a literal value
        return node

#-------------------------------------------------------------------------------

def run(file_name):
    with open(file_name) as f:
        code = f.read().replace('\n', '')
    for block in parser.parse(code):
        exec(gen(block), namespace)
