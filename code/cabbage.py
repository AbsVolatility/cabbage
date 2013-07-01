#-------------------------------------------------------------------------------
# Code generator and executer for the Cabbage language
#-------------------------------------------------------------------------------

from __future__ import print_function

from cbg_lexer import lexer
from cbg_parser import parser

from cbg_builtins import *
from cbg_operators import *

namespace = {'__builtins__': {'print': print},
             '_': base}

def gen(node):
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
        return ''
    elif node_type == 'binary_op':
        return eval('{}({!r}, {!r})'.format(node.op, gen(node.arg1), gen(node.arg2)), globals())
    elif node_type == 'unary_op':
        return eval('{}({!r})'.format(node.op, gen(node.arg)), globals())
    elif node_type == 'function':
        return '{}(*{})'.format(node.name, gen(node.param_list))
    else:  # a literal value
        return node

#-------------------------------------------------------------------------------

def run(file_name):
    with open(file_name) as f:
        for line in f:
            code = code.rstrip(' \n')
            if code:
                exec(gen(parser.parse(code)), namespace)
