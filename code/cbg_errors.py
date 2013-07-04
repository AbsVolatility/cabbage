class CbgException(Exception):
    pass

class CbgTypeError(CbgException):
    type = 'TypeError'

class CbgValueError(CbgException):
    type = 'ValueError'

class CbgSyntaxError(CbgException):
    type = 'SyntaxError'