class cbgInteger:
    type = 'integer'
    def __init__(self, value):
        self.value = int(value)
        self.out = self.value
    def __repr__(self):
        return 'cbgInteger({!r})'.format(self.value)

class cbgFloat:
    type = 'float'
    def __init__(self, value):
        self.value = float(value)
        self.out = self.value
    def __repr__(self):
        return 'cbgFloat({!r})'.format(self.value)

class cbgBool:
    type = 'bool'
    def __init__(self, value):
        self.value = value
        self.out = {True: 'true', False: 'false'}[value]
        self.repr_ = self.out
    def __repr__(self):
        return 'cbgBool({!r})'.format(self.value)

class cbgString:
    type = 'string'
    def __init__(self, value):
        self.value = list(value)
        self.out = ''.join(self.value)
    def __repr__(self):
        return 'cbgString({!r})'.format(self.out)

class cbgList:
    type = 'list'
    def __init__(self, value):
        self.value = list(value)
        self.out = self.value
    def __repr__(self):
        return 'cbgList({!r})'.format(self.value)

class cbgFunction:
    type = 'function'
    def __init__(self, value):
        self.value = value
        self.out = 'a function'
        self.repr_ = self.out
    def __repr__(self):
        return 'cbgFunction({!r})'.format(self.value)

class cbgNone:
    type = 'none'
    def __init__(self):
        self.value = None
        self.out = 'none'
        self.repr_ = self.out
    def __repr__(self):
        return 'cbgNone()'
    def __bool__(self):
        return False