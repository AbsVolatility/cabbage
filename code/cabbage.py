#-------------------------------------------------------------------------------
# Code generator and interpreter for the Cabbage language
#-------------------------------------------------------------------------------

from cbg_lexer import lexer
from cbg_parser import parser

from cbg_builtins import *

full_namespace = {'__builtins__': {'print': print}, '_': full_base}
support_namespace = {'__builtins__': {'print': print}, 'base': support_base}
rebel_namespace = {'__builtins__': {'print': print}, 'base': rebel_base}
namespaces = {'full': full_namespace,
              'support': support_namespace,
              'rebel': rebel_namespace}
namespace = namespaces['full']
mode = 'full'

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
        pre = "'All Hail Brassica Prime!', " if mode == 'support' \
              else "'Death to Cabbage!', " if mode == 'rebel' else ''
        return "print({}{!r})".format(pre, gen(node.value))
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
    elif node_type == 'expression':
        return 'print("{!r}")'.format(gen(node.value))
    elif node_type == 'binary_op':
        op, arg1, arg2 = node.op, gen(node.arg1), gen(node.arg2)
        if not isinstance(arg1, (int, float)) or not isinstance(arg2, (int, float)):
            return Error()  # <-
        if op == '/' and mode == 'rebel':
            op = '//'
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
        if s in ('fully support!', 'support!', 'rebel!'):
            if s == 'fully support!':
                mode = 'full'
            else:
                mode = s[:-1]
            lexer.begin(mode)
            namespace = namespaces[mode]
            continue
        parsed = parser.parse(s)
        code = gen(parsed)
        exec(str(code), namespace)

def execute(code):
    code = code.rstrip('\n')
    if code:
        exec(gen(parser.parse(code)), namespace)

def run(file_name):
    with open(file_name) as f:
        first_line = next(f).rstrip('\n')
        if first_line not in ('In favour of Cabbage:',
                              'In opposition to Cabbage:'):
            execute(first_line)
        else:
            mode = 'support' if 'f' in first_line else 'rebel'
            lexer.begin(mode)
        for line in f:
            execute(line)
