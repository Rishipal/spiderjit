__author__ = 'sarangis'

import ast
from functools import reduce

class CompareOps:
    LT = 0


class Var(ast.AST):
    _fields = ["id", "type"]

    def __init__(self, id, type=None):
        self.id = id
        self.type = type

    def __str__(self):
        return self.id

    __repr__ = __str__

class Assign(ast.AST):
    _fields = ["ref", "val", "type"]

    def __init__(self, ref, val, type=None):
        self.ref = ref
        self.val = val
        self.type = type

class Return(ast.AST):
    _fields = ["val"]

    def __init__(self, val):
        self.val = val

class Loop(ast.AST):
    _fields = ["var", "begin", "end", "body"]

    def __init__(self, var, begin, end, body):
        self.var = var
        self.begin = begin
        self.end = end
        self.body = body

class Compare(ast.AST):
    pass

class If(ast.AST):
    _fields = ["var", "begin", "end", "body"]

    def __init__(self, var, begin, end, body):
        self.var = var
        self.begin = begin
        self.end = end
        self.body = body

class App(ast.AST):
    _fields = ["fn", "args"]

    def __init__(self, fn, args):
        self.fn = fn
        self.args = args

class Func(ast.AST):
    _fields = ["fname", "args", "body"]

    def __init__(self, fname, args, body):
        self.fname = fname
        self.args = args
        self.body = body

class LitInt(ast.AST):
    _fields = ["s"]

    def __init__(self, s, type=None):
        self.s = s
        self.type = type

class LitFloat(ast.AST):
    _fields = ["s"]

    def __init__(self, s, type=None):
        self.s = s
        self.type = type

class LitBool(ast.AST):
    _fields = ["s"]

    def __init__(self, s):
        self.s = s


class LitString(ast.AST):
    _fields = ["n"]

    def __init__(self, s):
        self.s = s

class Prim(ast.AST):
    _fields = ["fn", "args"]

    def __init__(self, fn, args):
        self.fn = fn
        self.args = args

class Index(ast.AST):
    _fields = ["val", "ix"]

    def __init__(self, val, ix):
        self.val = val
        self.ix = ix

class Noop(ast.AST):
    _fields = []


#----------------------------------------------------------------------------------------------------------------------#

class IntTy(object):
    def __init__(self, s):
        self.s = s

    def __hash__(self):
        return hash(self.s)

    def __eq__(self, other):
        if isinstance(other, IntTy):
            return self.s == other.s
        else:
            return False

    def __str__(self):
        return "IntTy { " + str(self.s) + " }"

    __repr__ = __str__

class FloatTy(object):
    def __init__(self, s):
        self.s = s

    def __hash__(self):
        return hash(self.s)

    def __eq__(self, other):
        if isinstance(other, IntTy):
            return self.s == other.s
        else:
            return False

    def __str__(self):
        return "FloatTy { " + str(self.s) + " }"

    __repr__ = __str__

class BoolTy(object):
    def __init__(self, s):
        self.s = s

    def __hash__(self):
        return hash(self.s)

    def __eq__(self, other):
        if isinstance(other, IntTy):
            return self.s == other.s
        else:
            return False

    def __str__(self):
        return "BoolTy { " + str(self.s) + " }"

    __repr__ = __str__


class StringTy(object):
    def __init__(self, s):
        self.s = s

    def __hash__(self):
        return hash(self.s)

    def __eq__(self, other):
        if isinstance(other, IntTy):
            return self.s == other.s
        else:
            return False

    def __str__(self):
        return "StringTy { " + str(self.s) + " }"

    __repr__ = __str__


class VarTy(object):
    def __init__(self, s):
        self.s = s

    def __hash__(self):
        return hash(self.s)

    def __eq__(self, other):
        if isinstance(other, VarTy):
            return self.s == other.s
        else:
            return False

    def __str__(self):
        return "VarTy{ " + str(self.s) + " }"

    __repr__ = __str__


class ListTy(object):
    def __init__(self, s):
        self.s = s

    def __hash__(self):
        return hash(self.s)

    def __eq__(self, other):
        if isinstance(other, VarTy):
            return self.s == other.s
        else:
            return False

    def __str__(self):
        return "ListTy {" + str(self.s) + " }"

    __repr__ = __str__


class DictTy(object):
    def __init__(self, s):
        self.s = s

    def __hash__(self):
        return hash(self.s)

    def __eq__(self, other):
        if isinstance(other, VarTy):
            return self.s == other.s
        else:
            return False

    def __str__(self):
        return "DictTy {" + str(self.s) + " }"

    __repr__ = __str__


class TupleTy(object):
    def __init__(self, s):
        self.s = s

    def __hash__(self):
        return hash(self.s)

    def __eq__(self, other):
        if isinstance(other, VarTy):
            return self.s == other.s
        else:
            return False

    def __str__(self):
        return "TupleTy {" + str(self.s) + " }"

    __repr__ = __str__


class ConstructorTy(object):
    def __init__(self, s):
        self.s = s

    def __hash__(self):
        return hash(self.s)

    def __eq__(self, other):
        if isinstance(other, ConstructorTy):
            return (self.s == other.s)
        else:
            return False

    def __str__(self):
        return "ConstructorTy {" + str(self.s) + " }"

    __repr__ = __str__


class AppTy(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        if isinstance(other, AppTy):
            return (self.a == other.a) and (self.b == other.b)
        else:
            return False

    def __hash__(self):
        return hash((self.a, self.b))

    def __str__(self):
        return str(self.a) + " " + str(self.b)

    __repr__ = __str__

class FuncTy(object):
    def __init__(self, argsTys, retTy):
        self.argTys = argsTys
        self.retTy = retTy

    def __eq__(self, other):
        if isinstance(other, FuncTy):
            return (self.argTys == other.argTys) & (self.retty == other.retTy)
        else:
            return False

    def __str__(self):
        return str(self.argTys) + " -> " + str(self.retTy)

    __repr__ = __str__



from functools import reduce
def ftv(x):
    if isinstance(x, ConstructorTy):
        return set()
    elif isinstance(x, AppTy):
        return ftv(x.a) | ftv(x.b)
    elif isinstance(x, FuncTy):
        return reduce(set.union, map(ftv, x.argTys)) | ftv(x.retTy)
    elif isinstance(x, VarTy):
        return set([x])

def is_array(ty):
    return isinstance(ty, AppTy) and ty.a == ConstructorTy("Array")

int32 = ConstructorTy("Int32")
int64 = ConstructorTy("Int64")
float32 = ConstructorTy("Float")
double64 = ConstructorTy("Double")
void = ConstructorTy("Void")
array = lambda t: AppTy(ConstructorTy("Array"), t)

array_int32 = array(int32)
array_int64 = array(int64)
array_double64 = array(double64)