#-------------------------------------------------------------------------------
# Code generator and executer for the Cabbage language
#-------------------------------------------------------------------------------

from __future__ import print_function

from cbg_lexer import lexer
from cbg_parser import parser

from cbg_builtins import funcs, types

namespace = {'__builtins__': funcs}

namespace['__builtins__'].update(types)

def indent(lst):
    def ind(lst, lvl=0):
        indented = []
        for i in lst:
            if isinstance(i, list):
                indented.extend(ind(i, lvl=lvl+4))
            else:
                indented.append(' '*lvl + i.replace('\n', '\n'+' '*lvl))
        return indented
    return '\n'.join(ind(lst))

def gen(node, print_expr=False, el=False):
    node_type = node.type
    if node_type == 'assign':
        name = node.name
        if name == '__builtins__':
            raise NameError("Can't assign to '__builtins__'")
        else:
            return '{} = {}'.format(name, gen(node.value))
    elif node_type == 'print':
        return '{}.print()'.format(gen(node.value))
    elif node_type == 'id':
        return node.name
    elif node_type == 'expression':
        return '{}.print(repr=True)'.format(gen(node.value)) if print_expr else 'pass'
    elif node_type == 'fold':
        return '{}.fold({!r})'.format(gen(node.lst), node.op)
    elif node_type == 'binary_op':
        return '{}.{}({})'.format(gen(node.arg1), node.op, gen(node.arg2))
    elif node_type == 'unary_op':
        return '{}({})'.format(node.op, gen(node.arg)) if node.isfunc else '{}.{}()'.format(gen(node.arg), node.op)
    elif node_type == 'lambdadef':
        return 'func(lambda {}: {})'.format(', '.join(node.vars), gen(node.code))
    elif node_type == 'functiondef':
        return indent(['def {}({}):'.format(node.name, ', '.join(node.vars)), gen(node.code) + ['return none'], "{0} = func('{0}', {0})".format(node.name)])
    elif node_type == 'functioncall':
        return '{}({})'.format(gen(node.func), gen(node.param_lst))
    elif node_type == 'paramlist':
        return ', '.join([str(gen(i)) for i in node.value])
    elif node_type == 'return':
        return 'return {}'.format(gen(node.value))
    elif node_type == 'break':
        return 'break'
    elif node_type == 'ifs':
        code = [gen(node.if_blocks[0])] + [gen(i, el=True) for i in node.if_blocks[1:]]
        if node.else_block is not None:
            code += [indent(['else:', gen(node.else_block)])]
        return '\n'.join(code)
    elif node_type == 'if':
        return indent(['{}if {}.value:'.format('el' if el else '', gen(node.cond)), gen(node.if_block)])
    elif node_type == 'ternary':
        return '(({}) if ({}.value) else ({}))'.format(gen(node.if_block), gen(node.cond), gen(node.else_block))
    elif node_type == 'for':
        return indent(['for {} in {}.value:'.format(node.id, gen(node.lst)), gen(node.code)])
    elif node_type == 'while':
        return indent(['while {}.value:'.format(gen(node.cond)), gen(node.code)])
    elif node_type == 'block':
        return [gen(i) for i in node.code]
    elif node_type in ('list', 'tuple', 'set'):
        return '{}([{}])'.format(node_type, ', '.join([str(gen(i)) for i in node.value]))
    elif node_type == 'slice':
        return '{}.slce({})'.format(gen(node.lst), gen(node.index))
    elif node_type == 'slce':
        return 'list([{}, {}, {}])'.format(gen(node.start), gen(node.stop), gen(node.step))
    elif node_type == 'listcomp':
        return 'list([{} {} if {}.value])'.format(gen(node.expr), ' '.join('for {} in {}.value'.format(id, gen(lst)) for id, lst in node.lists), 'true' if node.guard is None else gen(node.guard))
    else:  # a literal value
        return node

#-------------------------------------------------------------------------------

def run(file_name):
    with open(file_name) as f:
        code = f.read().replace('\n', '')
    try:
        for block in parser.parse(code).code:
            exec(gen(block), namespace)
    except Exception as e:
        print('{}: {}'.format(type(e).__name__, str(e)))
