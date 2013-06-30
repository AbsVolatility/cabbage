class cbgInteger:
    type = 'integer'
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'cbgInteger({!r})'.format(self.value)
    def __str__(self):
        return str(self.value)

class cbgFloat:
    type = 'float'
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'cbgFloat({!r})'.format(self.value)
    def __str__(self):
        return str(self.value)

class cbgBool:
    type = 'bool'
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'cbgBool({!r})'.format(self.value)
    def __str__(self):
        return str(self.value)

class cbgString:
    type = 'string'
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'cbgString({!r})'.format(self.value)
    def __str__(self):
        return repr(self.value)

class cbgList:
    type = 'list'
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'cbgList({!r})'.format(self.value)
    def __str__(self):
        return str(self.value)
