def unary(fn):
    def err(self):
        raise TypeError("unary operator '{}' not defined for type '{}'".format(fn(self), self.type))
    return err
def binary(fn):
    def err(self, other):
        raise TypeError("binary operator '{}' not defined for types '{}' and '{}'".format(fn(self, other), self.type, other.type))
    return err

class cbgType:
    def display(self, rout=False):
        print(self.rout if rout and hasattr(self, 'rout') else self.out)

    def uplus(self):
        return self
    def blnot(self):
        return cbgbool(not self.value)
    def eq(self, other):
        return cbgbool(self.value == other.value)
    def ne(self, other):
        return cbgbool(self.value != other.value)
    def bland(self, other):
        if not self.value:
            return self
        else:
            return other
    def blor(self, other):
        if self.value:
            return self
        else:
            return other
    def slce(self, index):
        raise TypeError("'{}' object is not subscriptable".format(self.type))
    @unary
    def uminus(self): return '-'
    @unary
    def abs(self): return '|'
    @unary
    def sgn(self): return '*'
    @unary
    def bwnot(self): return '.~'
    @binary
    def add(self, other): return '+'
    @binary
    def sub(self, other): return '-'
    @binary
    def mul(self, other): return '*'
    @binary
    def div(self, other): return '/'
    @binary
    def pow(self, other): return '^'
    @binary
    def mod(self, other): return '%'
    @binary
    def map(self, lst): return '#'
    @binary
    def fold(self, op): return '/'
    @binary
    def bwand(self, other): return '.&'
    @binary
    def bwor(self, other): return '.|'
    @binary
    def bwxor(self, other): return '.^'
    @binary
    def lt(self, other): return '<'
    @binary
    def le(self, other): return '<='
    @binary
    def ge(self, other): return '>='
    @binary
    def gt(self, other): return '>'
    @binary
    def rnge(self, other): return '..'

class cbgNumber(cbgType):
    def __init__(self, value, tp):
        tpfunc = int if tp=='integer' else float
        if hasattr(value, 'type'):
            if value.type in ('integer', 'float', 'string', 'bool'):
                self.value = tpfunc(value.value)
            else:
                raise TypeError("can't convert type '{}' into {}".format(value.type, tp))
        else:
            self.value = tpfunc(value)
        self.out = str(self.value)

    def uminus(self):
        return self.__class__(-self.value)
    def abs(self):
        return self.__class__(self.sgn().value * self.value)
    def sgn(self):
        return cbgInteger(1 if self.value > 0 else -1 if self.value < 0 else 0)
    def lt(self, other):
        if other.type in ('integer', 'float'):
            return cbgbool(self.value < other.value)
        else:
            super().lt(other)
    def le(self, other):
        if other.type in ('integer', 'float'):
            return cbgbool(self.value <= other.value)
        else:
            super().le(other)
    def ge(self, other):
        if other.type in ('integer', 'float'):
            return cbgbool(self.value >= other.value)
        else:
            super().ge(other)
    def gt(self, other):
        if other.type in ('integer', 'float'):
            return cbgbool(self.value > other.value)
        else:
            super().gt(other)

class cbgSequence(cbgType):
    def uminus(self):
        return self.__class__(self.value[::-1])
    def abs(self):
        return cbgInteger(len(self.value))
    def add(self, other):
        return self.__class__(self.value + self.__class__(other).value)
    def mul(self, other):
        if other.type == 'integer':
            return self.__class__(self.value * other.value)
        elif other.type in ('string', 'list', 'tuple'):
            return cbgList([cbgTuple(i.add(j)) if i.type=='tuple' else cbgTuple((i, j)) for i in self.value for j in other.value])
        else:
            super().mul(other)
    def pow(self, other):
        if other.type == 'integer':
            if other.value >= 1:
                val = self
                for _ in range(other.value-1):
                    val = val.mul(self)
                return val
            else:
                raise ValueError('power of a sequence must be a positive integer')
        else:
            super().pow(other)
    def slce(self, index):
        if index.type == 'integer':
            return self.value[index.value]
        elif index.type == 'list':
            if not all(i.type in ('integer', 'none') for i in index.value):
                raise TypeError("slice values must be integers or 'none'")
            return self.__class__(self.value[slice(*[i.value for i in index.value])])
        else:
            raise TypeError("invalid index type '{}'".format(index.type))

class cbgInteger(cbgNumber):
    type = 'integer'
    def __init__(self, value):
        super().__init__(value, 'integer')
    def __repr__(self):
        return 'int({!r})'.format(self.value)

    def add(self, other):
        if other.type in ('integer', 'float'):
            return other.__class__(self.value + other.value)
        elif other.type in ('string', 'list', 'tuple'):
            return other.__class__(self).add(other)
        else:
            super().add(self, other)
    def sub(self, other):
        if other.type in ('integer', 'float'):
            return other.__class__(self.value - other.value)
        else:
            super().sub(self, other)
    def mul(self, other):
        if other.type in ('integer', 'float', 'string', 'list'):
            return other.__class__(self.value * other.value)
        else:
            super().mul(self, other)
    def div(self, other):
        if other.type == 'integer' and self.mod(other).value == 0:
            return cbgInteger(self.value // other.value)
        elif other.type in ('integer', 'float'):
            return cbgFloat(self.value / other.value)
        else:
            super().div(self, other)
    def pow(self, other):
        if other.type in ('integer', 'float'):
            return other.__class__(self.value ** other.value)
        else:
            super().pow(self, other)
    def mod(self, other):
        if other.type in ('integer', 'float'):
            return other.__class__(self.value % other.value)
        else:
            super().mod(self, other)
    def bwand(self, other):
        if other.type == 'integer':
            return cbgInteger(self.value & other.value)
        else:
            super().bwand(self, other)
    def bwor(self, other):
        if other.type == 'integer':
            return cbgInteger(self.value | other.value)
        else:
            super().bwor(self, other)
    def bwxor(self, other):
        if other.type == 'integer':
            return cbgInteger(self.value ^ other.value)
        else:
            super().bwxor(self, other)
    def bwnot(self):
        return cbgInteger(~self.value)
    def rnge(self, other):
        if other.type == 'integer':
            return cbgList([cbgInteger(i) for i in range(self.value, other.value+1)])
        else:
            super().rnge(self, other)

class cbgFloat(cbgNumber):
    type = 'float'
    def __init__(self, value):
        super().__init__(value, 'float')
    def __repr__(self):
        return 'float({!r})'.format(self.value)

    def add(self, other):
        if other.type in ('integer', 'float'):
            return cbgFloat(self.value + other.value)
        elif other.type in ('string', 'list', 'tuple'):
            return other.__class__(self).add(other)
        else:
            super().add(self, other)
    def sub(self, other):
        if other.type in ('integer', 'float'):
            return cbgFloat(self.value - other.value)
        else:
            super().sub(self, other)
    def mul(self, other):
        if other.type in ('integer', 'float'):
            return cbgFloat(self.value * other.value)
        else:
            super().mul(self, other)
    def div(self, other):
        if other.type in ('integer', 'float'):
            return cbgFloat(self.value / other.value)
        else:
            super().div(self, other)
    def pow(self, other):
        if other.type in ('integer', 'float'):
            return cbgFloat(self.value ** other.value)
        else:
            super().pow(self, other)
    def mod(self, other):
        if other.type in ('integer', 'float'):
            return cbgFloat(self.value % other.value)
        else:
            super().mod(self, other)

class cbgString(cbgSequence):
    type = 'string'
    def __init__(self, value):
        self.value = value.out if hasattr(value, 'type') else value
        self.out = self.value
        self.rout = repr(self.out)
    def __repr__(self):
        return 'str({!r})'.format(self.out)

    def add(self, other):
        if other.type == 'string':
            return cbgString(self.value + other.value)
        if other.type in ('integer', 'float'):
            return cbgString(self.value + other.out)
        else:
            super().add(self, other)
    def mul(self, other):
        cbgType.mul(self, other)
    def pow(self, other):
        cbgType.pow(self, other)
    def slce(self, index):
        if index.type == 'integer':
            return cbgString(self.value[index.value])
        if index.type == 'list':
            if not all(i.type in ('integer', 'none') for i in index.value):
                raise TypeError("slice values must be integers or 'none'")
            return cbgString(self.value[slice(*[i.value for i in index.value])])
        else:
            raise TypeError("invalid index type '{}'".format(index.type))

class cbgList(cbgSequence):
    type = 'list'
    def __init__(self, value):
        if hasattr(value, 'type') and value.type not in ('string', 'list', 'tuple'):
            self.value = [value]
        elif hasattr(value, 'value'):
            self.value = list(value.value)
        else:
            self.value = list(value)
    @property
    def out(self):
        return '[' + ', '.join([i.out for i in self.value]) + ']'
    def __repr__(self):
        return 'list({!r})'.format(self.value)
    def setslce(self, index, value):
        if index.type == 'integer':
            self.value[index.value] = value
        elif index.type == 'list':
            if not all(i.type in ('integer', 'none') for i in index.value):
                raise TypeError("slice values must be integers or 'none'")
            self.value[slice(*[i.value for i in index.value])] = value.value
        else:
            raise TypeError("invalid index type '{}'".format(index.type))

    def fold(self, op):
        val = self.value[0]
        for i in self.value[1:]:
            val = getattr(val, op)(i)
        return val

class cbgTuple(cbgSequence):
    type = 'tuple'
    def __init__(self, value):
        if hasattr(value, 'type') and value.type not in ('string', 'list', 'tuple'):
            self.value = (value,)
        elif hasattr(value, 'value'):
            self.value = tuple(value.value)
        else:
            self.value = tuple(value)
    @property
    def out(self):
        return '(' + ', '.join([i.out for i in self.value]) + ')'
    def __repr__(self):
        return 'tuple({!r})'.format(self.value)

    def fold(self, op):
        val = self.value[0]
        for i in self.value[1:]:
            val = getattr(val, op)(i)
        return val

class cbgSet(cbgType):
    type = 'set'
    def __init__(self, value):
        if hasattr(value, 'type') and value.type not in ('list', 'set'):
            self.value = {value}
        elif hasattr(value, 'value'):
            self.value = set(value.value)
        else:
            self.value = set(value)
    @property
    def out(self):
        return '{' + ', '.join([i.out for i in sorted(self.value, key=lambda i:i.value)]) + '}'
    def __repr__(self):
        return 'set({!r})'.format(self.value)

    def abs(self):
        return cbgInteger(len(self.value))

class cbgFunction(cbgType):
    type = 'function'
    def __init__(self, name, value):
        if not callable(value):
            self.value = lambda: value
        else:
            self.value = value.value if hasattr(value, 'type') else value
        self.name = name
        self.out = "function '{}'".format(name)
    def __repr__(self):
        return 'func({!r})'.format(self.value)
    def __call__(self, *args, **kwargs):
        return self.value(*args, **kwargs)

    def div(self, lst):
        if lst.type == 'list':
            val = lst.value[0]
            for i in lst.value[1:]:
                val = self.value(val, i)
            return val
        else:
            super().div(self, lst)
    def map(self, lst):
        if lst.type == 'list':
            return cbgList([self.value(i) for i in lst.value])
        else:
            super().map(self, lst)

class cbgBool(cbgType):
    type = 'bool'
    def __init__(self, value):
        self.value = value
        self.out = ['false', 'true'][value]
    def __repr__(self):
        return self.out

class cbgNone(cbgType):
    type = 'none'
    def __init__(self):
        self.value = None
        self.out = 'none'
    def __repr__(self):
        return 'none'

true, false = cbgBool(True), cbgBool(False)
def cbgbool(val):
    return (false, true)[val]

none = cbgNone()

types = {'int': cbgInteger, 'float': cbgFloat,
         'str': cbgString, 'list': cbgList, 'tuple': cbgTuple, 'set': cbgSet,
         'func': cbgFunction,
         'bool': cbgbool, 'true': true, 'false': false,
         'none': none}