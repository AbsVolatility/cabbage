class cbgType:
    def unary(fn):
        def err(self):
            raise TypeError("unary operator '{}' not defined for type '{}'".format(fn(self), self.type))
        return err
    def binary(fn):
        def err(self, other):
            raise TypeError("binary operator '{}' not defined for types '{}' and '{}'".format(fn(self, other), self.type, other.type))
        return err

    def print(self, repr=False):
        print(self.repr if repr else self.out)

    def uplus(self):
        return self
    def blnot(self):
        return cbgbool(not self.value)
    def rpr(self):
        return cbgString(self.repr)
    def eq(self, other):
        return cbgbool(self.value == other.value)
    def ne(self, other):
        return cbgbool(self.value != other.value)
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
    def bland(self, other): return '&&'
    @binary
    def blor(self, other): return '||'
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

class cbgInteger(cbgType):
    type = 'integer'
    def __init__(self, value):
        if hasattr(value, 'type'):
            if value.type in ('integer', 'float', 'string', 'bool'):
                self.value = int(value.value)
            else:
                raise TypeError("can't convert type '{}' into integer".format(value.type))
        else:
            self.value = int(value)
        self.out = str(self.value)
        self.repr = self.out
    def __repr__(self):
        return 'int({!r})'.format(self.value)

    def uminus(self):
        return cbgInteger(-self.value)
    def abs(self):
        return cbgInteger(self.sgn().value * self.value)
    def sgn(self):
        return cbgInteger(1) if self.value > 0 else cbgInteger(-1) if self.value < 0 else cbgInteger(0)
    def add(self, other):
        if other.type in ('integer', 'float'):
            return other.__class__(self.value + other.value)
        elif other.type in ('string', 'list'):
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
    def lt(self, other):
        if other.type in ('integer', 'float'):
            return cbgBool(self.value < other.value)
        else:
            super().lt(self, other)
    def le(self, other):
        if other.type in ('integer', 'float'):
            return cbgBool(self.value <= other.value)
        else:
            super().le(self, other)
    def ge(self, other):
        if other.type in ('integer', 'float'):
            return cbgBool(self.value >= other.value)
        else:
            super().ge(self, other)
    def gt(self, other):
        if other.type in ('integer', 'float'):
            return cbgBool(self.value > other.value)
        else:
            super().gt(self, other)
    def rnge(self, other):
        if other.type == 'integer':
            return cbgList([cbgInteger(i) for i in range(self.value, other.value+1)])
        else:
            super().rnge(self, other)

class cbgFloat(cbgType):
    type = 'float'
    def __init__(self, value):
        if hasattr(value, 'type'):
            if value.type in ('integer', 'float', 'string', 'bool'):
                self.value = float(value.value)
            else:
                raise TypeError("can't convert type '{}' into float".format(value.type))
        else:
            self.value = float(value)
        self.out = str(self.value)
        self.repr = self.out
    def __repr__(self):
        return 'float({!r})'.format(self.value)

    def uminus(self):
        return cbgFloat(-self.value)
    def abs(self):
        return cbgFloat(self.sgn().value * self.value)
    def sgn(self):
        return cbgInteger(1) if self.value > 0 else cbgInteger(-1) if self.value < 0 else cbgInteger(0)
    def add(self, other):
        if other.type in ('integer', 'float'):
            return cbgFloat(self.value + other.value)
        elif other.type in ('string', 'list'):
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
    def lt(self, other):
        if other.type in ('integer', 'float'):
            return cbgBool(self.value < other.value)
        else:
            super().lt(self, other)
    def le(self, other):
        if other.type in ('integer', 'float'):
            return cbgBool(self.value <= other.value)
        else:
            super().le(self, other)
    def ge(self, other):
        if other.type in ('integer', 'float'):
            return cbgBool(self.value >= other.value)
        else:
            super().ge(self, other)
    def gt(self, other):
        if other.type in ('integer', 'float'):
            return cbgBool(self.value > other.value)
        else:
            super().gt(self, other)

class cbgString(cbgType):
    type = 'string'
    def __init__(self, value):
        self.value = value.out if hasattr(value, 'type') else value
        self.out = self.value
        self.repr = repr(self.out)
    def __repr__(self):
        return 'str({!r})'.format(self.out)

    def uminus(self):
        return cbgString(self.value[::-1])
    def abs(self):
        return cbgInteger(len(self.value))
    def add(self, other):
        if other.type == 'string':
            return cbgString(self.value + other.value)
        if other.type in ('integer', 'float'):
            return cbgString(self.value + other.out)
        else:
            super().add(self, other)
    def mul(self, other):
        if other.type == 'integer':
            return cbgString(self.value * other.value)
        else:
            super().mul(self, other)
    def slce(self, index):
        if index.type == 'integer':
            return cbgString(self.value[index.value])
        if index.type == 'list':
            if not all(i.type in ('integer', 'none') for i in index.value):
                raise TypeError("slice values must be integers or 'none'")
            return cbgString(self.value[slice(*[i.value for i in index.value])])
        else:
            raise TypeError("invalid index type '{}'".format(index.type))

class cbgList(cbgType):
    type = 'list'
    def __init__(self, value):
        if hasattr(value, 'type') and value.type not in ('string', 'list'):
            self.value = [value]
        else:
            self.value = list(value)
    @property
    def out(self):
        return str([i.value for i in self.value])
    @property
    def repr(self):
        return self.out
    def __repr__(self):
        return 'list({!r})'.format(self.value)

    def uminus(self):
        return cbgList(self.value[::-1])
    def abs(self):
        return cbgInteger(len(self.value))
    def add(self, other):
        if other.type == 'list':
            return cbgList(self.value + other.value)
        else:
            return cbgList(self.value + [other])
    def mul(self, other):
        if other.type == 'integer':
            return cbgList(self.value * other.value)
        else:
            super().mul(self, other)
    def fold(self, op):
        val = self.value[0]
        for i in self.value[1:]:
            val = getattr(val, op)(i)
        return val
    def slce(self, index):
        if index.type == 'integer':
            return self.value[index.value]
        if index.type == 'list':
            if not all(i.type in ('integer', 'none') for i in index.value):
                raise TypeError("slice values must be integers or 'none'")
            return cbgList(self.value[slice(*[i.value for i in index.value])])
        else:
            raise TypeError("invalid index type '{}'".format(index.type))

class cbgFunction(cbgType):
    type = 'function'
    def __init__(self, value):
        if not callable(value):
            self.value = lambda: value
        else:
            self.value = value.value if hasattr(value, 'type') else value
        self.out = 'a function'
        self.repr = self.out
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
        self.repr = self.out
    def __repr__(self):
        return self.out

    def bland(self, other):
        if other.type == 'bool':
            return cbgbool(self.value and other.value)
        else:
            super().bland(self, other)
    def blor(self, other):
        if other.type == 'bool':
            return cbgbool(self.value or other.value)
        else:
            super().blor(self, other)

class cbgNone(cbgType):
    type = 'none'
    def __init__(self):
        self.value = None
        self.out = 'none'
        self.repr = self.out
    def __repr__(self):
        return 'none'

true = cbgBool(True)
false = cbgBool(False)
def cbgbool(val):
    return (false, true)[bool(val)]

none = cbgNone()

types = {'int': cbgInteger,
         'float': cbgFloat,
         'str': cbgString,
         'list': cbgList,
         'func': cbgFunction,
         'bool': cbgbool,
         'true': true,
         'false': false,
         'none': none}