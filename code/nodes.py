class Node:
    pass

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
        return 'Expr({!r})'.format(self.value)

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
                   '%': 'mod',
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

class FunctionDef(Node):
    type = 'functiondef'
    def __init__(self, vars, code):
        self.vars = vars
        self.code = code
    def __repr__(self):
        return 'Function({!r}, {!r})'.format(self.vars, self.code)

class FunctionCall(Node):
    type = 'functioncall'
    def __init__(self, func, param_lst):
        self.func = {'input': 'input_'}.get(func, func)
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

class For(Node):
    type = 'for'
    def __init__(self, id, lst, code):
        self.id = id
        self.lst = lst
        self.code = code
    def __repr__(self):
        return 'For({!r}, {!r}, {!r})'.format(self.id, self.lst, self.code)

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