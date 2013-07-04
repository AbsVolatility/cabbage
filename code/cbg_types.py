class cbgInteger:
    type = 'integer'
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'cbgInteger({!r})'.format(self.value)

class cbgFloat:
    type = 'float'
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'cbgFloat({!r})'.format(self.value)

class cbgBool:
    type = 'bool'
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'cbgBool({!r})'.format(self.value)

class cbgString:
    type = 'string'
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'cbgString({!r})'.format(self.value)

class cbgList:
    type = 'list'
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'cbgList({!r})'.format(self.value)

class cbgFunction:
    type = 'function'
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'cbgFunction({!r})'.format(self.value)

class cbgNone:
    type = 'none'
    def __init__(self):
        self.value = None
    def __repr__(self):
        return 'cbgNone()'
    def __bool__(self):
        return False

class cbgVar:
    type = 'var'
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'cbgVar({!r})'.format(self.value)