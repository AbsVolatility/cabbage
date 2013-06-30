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

class BinaryOp(Node):
    type = 'binary_op'
    def __init__(self, op, arg1, arg2):
        self.op = {'+': 'add',
                   '-': 'sub',
                   '*': 'mul',
                   '/': 'div',
                   '.@': 'lt',
                   '=@': 'le',
                   '@': 'eq',
                   '!@': 'ne',
                   '@=': 'ge',
                   '@.': 'gt'}.get(op, op)
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