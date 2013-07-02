class Node:
    pass

class New(Node):
    type = 'new'
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return 'New({}, {!r})'.format(self.name, self.value)

class Print(Node):
    type = 'print'
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'Print({!r})'.format(self.value)

class Assign(Node):
    type = 'assign'
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return 'Assign({}, {!r})'.format(self.name, self.value)

class Id(Node):
    type = 'id'
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return 'Id({!r})'.format(self.name)

class Expression(Node):
    type = 'expression'
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return repr(self.value)

class UnaryOp(Node):
    type = 'unary_op'
    def __init__(self, op, arg):
        self.op = {'+': 'uplus',
                   '-': 'uminus',
                   '~': 'bwnot',
                   '!': 'blnot'}.get(op, op)
        self.arg = arg
    def __repr__(self):
        return '({} {!r})'.format(self.op, self.arg)

class BinaryOp(Node):
    type = 'binary_op'
    def __init__(self, op, arg1, arg2):
        self.op = {'+': 'add',
                   '-': 'sub',
                   '*': 'mul',
                   '/': 'div',
                   '^': 'pow_',
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
                   '&': 'bland',
                   '|': 'blor',
                   '..': 'rnge'}.get(op, op)
        self.arg1 = arg1
        self.arg2 = arg2
    def __repr__(self):
        return '({!r} {} {!r})'.format(self.arg1, self.op, self.arg2)

class Function(Node):
    type = 'function'
    def __init__(self, name, param_lst):
        self.name = name
        self.param_lst = param_lst
    def __repr__(self):
        return '{}(*{})'.format(self.name, self.param_lst)

class If(Node):
    type = 'if'
    def __init__(self, cond, if_block, else_block):
        self.cond = cond
        self.if_block = if_block
        self.else_block = else_block
    def __repr__(self):
        return 'If({!r}, {!r}, {!r})'.format(self.cond, self.if_block, self.else_block)

class Ternary(Node):
    type = 'ternary'
    def __init__(self, cond, if_block, else_block):
        self.cond = cond
        self.if_block = if_block
        self.else_block = else_block
    def __repr__(self):
        return '({!r} ? {!r} : {!r})'.format(self.cond, self.if_block, self.else_block)

class Block(Node):
    type = 'block'
    def __init__(self, code):
        self.code = code
    def __repr__(self):
        return 'Block({})'.format(self.code)