class Node:
    pass

class Assign(Node):
    type = 'assign'
    def __init__(self, name, value):
        self.name = 'cbg_' + name
        self.value = value
    def __repr__(self):
        return 'Assign({}, {!r})'.format(self.name, self.value)

class IdxAssign(Node):
    type = 'idxassign'
    def __init__(self, lst, slce, value):
        self.lst = lst
        self.slce = slce
        self.value = value
    def __repr__(self):
        return 'IdxAssign({!r}, {!r}, {!r})'.format(self.lst, self.slce, self.value)

class Id(Node):
    type = 'id'
    def __init__(self, name, special=False):
        self.name = ('cbg_' if not special else '') + name
    def __repr__(self):
        return 'Id({!r})'.format(self.name)

class Expression(Node):
    type = 'expression'
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'Expr({!r})'.format(self.value)

class UnaryOp(Node):
    type = 'unary_op'
    def __init__(self, op, arg, isfunc=False):
        self.op = {'+': 'uplus',
                   '-': 'uminus',
                   '~': 'bwnot',
                   '!': 'blnot',
                   '|': 'abs',
                   '*': 'sgn',
                   '`': 'rpr'}.get(op, op)
        self.arg = arg
        self.isfunc = isfunc
    def __repr__(self):
        return '({} {!r})'.format(self.op, self.arg)

class BinaryOp(Node):
    type = 'binary_op'
    def __init__(self, op, arg1, arg2):
        self.op = {'+': 'add',
                   '-': 'sub',
                   '*': 'mul',
                   '/': 'div',
                   '^': 'pow',
                   '%': 'mod',
                   '#': 'map',
                   '<': 'lt',
                   '<=': 'le',
                   '=': 'eq',
                   '!=': 'ne',
                   '>=': 'ge',
                   '>': 'gt',
                   '.&': 'bwand',
                   '.|': 'bwor',
                   '.^': 'bwxor',
                   '~': 'bwnot',
                   '&&': 'bland',
                   '||': 'blor',
                   '..': 'rnge'}.get(op, op)
        self.arg1 = arg1
        self.arg2 = arg2
    def __repr__(self):
        return '({!r} {} {!r})'.format(self.arg1, self.op, self.arg2)

class Fold(Node):
    type = 'fold'
    def __init__(self, op, lst):
        self.op = {'+': 'add',
                   '-': 'sub',
                   '*': 'mul',
                   '/': 'div',
                   '^': 'pow',
                   '%': 'mod',
                   '.&': 'bwand',
                   '.|': 'bwor',
                   '.^': 'bwxor',
                   '&': 'bland',
                   '|': 'blor'}.get(op, op)
        self.lst = lst
    def __repr__(self):
        return 'Fold({!r}, {!r})'.format(self.op, self.lst)

class Slice(Node):
    type = 'slice'
    def __init__(self, lst, index):
        self.lst = lst
        self.index = index
    def __repr__(self):
        return 'Slice({!r}, {!r})'.format(self.lst, self.index)

class Slce(Node):
    type = 'slce'
    def __init__(self, start, stop, step):
        self.start = start
        self.stop = stop
        self.step = step
    def __repr__(self):
        return 'Slce({!r}, {!r}, {!r})'.format(self.start, self.stop, self.step)

class LambdaDef(Node):
    type = 'lambdadef'
    def __init__(self, var_lst, code):
        self.var_lst = var_lst
        self.code = code
    def __repr__(self):
        return 'Lambda({!r}, {!r})'.format(self.vars, self.code)

class FunctionDef(Node):
    type = 'functiondef'
    def __init__(self, name, var_lst, code):
        self.name = name
        self.var_lst = var_lst
        self.code = code
    def __repr__(self):
        return 'Function({!r}, {!r}, {!r})'.format(self.name, self.vars, self.code)

class FunctionCall(Node):
    type = 'functioncall'
    def __init__(self, func, param_lst):
        self.func = func
        self.param_lst = param_lst
    def __repr__(self):
        return '{}(*{})'.format(self.func, self.param_lst)

class ParamList(Node):
    type = 'paramlist'
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'ParamList({!r})'.format(self.value)

class Return(Node):
    type = 'return'
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'Return({!r})'.format(self.value)

class If(Node):
    type = 'if'
    def __init__(self, cond, if_block):
        self.cond = cond
        self.if_block = if_block
    def __repr__(self):
        return 'If({!r}, {!r})'.format(self.cond, self.if_block)

class Ifs(Node):
    type = 'ifs'
    def __init__(self, if_blocks, else_block):
        self.if_blocks = if_blocks
        self.else_block = else_block
    def __repr__(self):
        return 'Ifs({!r}, {!r})'.format(self.if_blocks, self.else_block)

def switchcase(expr, cases, default):
    return Ifs([If(BinaryOp('=', expr, val), code) for val, code in cases], default)

class Ternary(Node):
    type = 'ternary'
    def __init__(self, cond, if_block, else_block):
        self.cond = cond
        self.if_block = if_block
        self.else_block = else_block
    def __repr__(self):
        return '({!r} ? {!r} : {!r})'.format(self.cond, self.if_block, self.else_block)

class For(Node):
    type = 'for'
    def __init__(self, var, lst, code):
        self.var = var
        self.lst = lst
        self.code = code
    def __repr__(self):
        return 'For({!r}, {!r}, {!r})'.format(self.id, self.lst, self.code)

class Break(Node):
    type = 'break'
    def __repr__(self):
        return 'Break()'

class While(Node):
    type = 'while'
    def __init__(self, cond, code):
        self.cond = cond
        self.code = code
    def __repr__(self):
        return 'While({!r}, {!r})'.format(self.cond, self.code)

class Block(Node):
    type = 'block'
    def __init__(self, code):
        self.code = code
    def __repr__(self):
        return 'Block({})'.format(self.code)

class ListComp(Node):
    type = 'listcomp'
    def __init__(self, expr, lists, guard):
        self.expr = expr
        self.lists = [(node.name, node.value) for node in lists]
        self.guard = guard
    def __repr__(self):
        return 'ListComp({!r}, {!r}, {!r})'.format(self.expr, self.lists, self.guard)

class NoOp(Node):
    type = 'noop'
    def __repr__(self):
        return 'NoOp'