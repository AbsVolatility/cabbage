#-------------------------------------------------------------------------------
# Code generator and interpreter for the Cabbage language
#-------------------------------------------------------------------------------

from cbg_lexer import lexer
from cbg_parser import parser

from cbg_builtins import *

namespace = {'__builtins__': {'print': print}, '_': base}

def gen(node):
    node_type = node.type
    if node_type == 'new':
        name = node.name
        if name == '__builtins__':
            print("Can't assign to '__builtins__'")  # turn into error
            return ''
        else:
            return '{} = {!r}'.format(name, gen(node.value))
    elif node_type == 'print':
        return "print({!r})".format(gen(node.value))
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
    elif node_type == 'function':
        return '{}(*{})'.format(node.name, gen(node.param_list))
    elif node_type == 'id':
        return eval(node.name, namespace)
    elif node_type == 'binary_op':
        op, arg1, arg2 = node.op, gen(node.arg1), gen(node.arg2)
        if not isinstance(arg1, (int, float)) or not isinstance(arg2, (int, float)):
            return Error()  # <-
        return eval('{!r} {} {!r}'.format(arg1, op, arg2), namespace)
    elif node_type in ('number', 'string', 'list'):
        return node.value

#-------------------------------------------------------------------------------

def interpreter():
    global mode
    global namespace
    while True:
        s = input('@> ')
        if not s:
            continue
        parsed = parser.parse(s)
        if parsed.type == 'expression':
            code = 'print("{!r}")'.format(gen(parsed.value))
        else:
            code = gen(parsed)
        exec(str(code), namespace)

def run(file_name):
    with open(file_name) as f:
        for line in f:
            code = code.rstrip(' \n')
            if code:
                exec(gen(parser.parse(code)), namespace)
