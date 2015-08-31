__author__ = 'sarangis'

import string
from pyjit.nodes import *

def naming():
    k = 0
    while True:
        for a in string.ascii_lowercase:
            yield ("'" + a + str(k)) if (k > 0) else (a)

class InferType(object):
    def __init__(self):
        self.constraints = []
        self.env = {}
        self.names = naming()

    def fresh(self):
        return VarTy('$' + next(self.names))

    def visit(self, node):
        name = "visit_%s" % type(node).__name__
        if hasattr(self, name):
            return getattr(self, name)(node)
        else:
            return self.generic_visit(node)

    def visit_Func(self, node):
        arity = len(node.args)
        self.argTys = [self.fresh()  for v in node.args]
        self.retTy = VarTy("$retTy")
        for (arg, ty) in zip(node.args, self.argTys):
            arg.type = ty
            self.env[arg.id] = ty

        for n in node.body: self.visit(n)
        return FuncTy(self.argTys, self.retTy)

    def visit_Noop(self, node):
        return None

    def visit_LitInt(self, node):
        #tv = self.fresh()
        node.type = IntTy(node.s)
        return node.type

    def visit_LitFloat(self, node):
        #tv = self.fresh()
        node.type = FloatTy(node.s)
        return node.type

    def visit_LitBool(self, node):
        #tv = self.fresh()
        node.type = BoolTy(node.s)
        return node.type

    def visit_LitString(self, node):
        node.type = StringTy(node.s)
        return node.type

    def visit_Assign(self, node):
        ty = self.visit(node.val)
        if node.ref in self.env:
            # Subsequent uses of a variable must have same type
            self.constraints += [(ty, self.env[node.ref])]

        self.env[node.ref] = ty
        node.ref = ty
        return None

    def visit_Index(self, node):
        tv = self.fresh()
        ty = self.visit(node.val)
        ixty = self.visit(node.ix)
        self.constraints += [(ty, array(tv)), (ixty, int32)]
        return tv

    def visit_Prim(self, node):
        if node.fn == "shape#":
            return array(int32)
        elif node.fn == "mult#" or node.fn == "add#":
            tya = self.visit(node.args[0])
            tyb = self.visit(node.args[1])
            self.constraints += [(tya, tyb)]
            return tyb
        else:
            raise NotImplementedError

    def visit_Var(self, node):
        ty = self.env[node.id]
        node.type = ty
        return ty

    def visit_Return(self, node):
        ty = self.visit(node.val)
        self.constraints += [(ty, self.retTy)]

    def visit_Loop(self, node):
        self.env[node.var.id] = int32
        varTy = self.visit(node.var)
        begin = self.visit(node.begin)
        end = self.visit(node.end)
        self.constraints += [(varTy, int32), (begin, int64), (end, int32)]
        for n in node.body: self.visit(n)

    def generic_visit(self, node):
        raise NotImplementedError("Visitor class doesn't implement %s" % type(node))

#----------------------------------------------------------------------------------------------------------------------#
from collections import deque

class TypeSolver:
    def __init__(self):
        pass

    @staticmethod
    def solve(type_constraints):
        constraints = deque(type_constraints)
        while len(constraints) > 0:
            constraint = constraints.popleft()
            print(constraint)

#----------------------------------------------------------------------------------------------------------------------#

from pyjit.nodes import *
from collections import deque

def empty():
    return {}


def apply(s, t):
    if isinstance(t, ConstructorTy):
        return t
    elif isinstance(t, AppTy):
        return AppTy(apply(s, t.a), apply(s, t.b))
    elif isinstance(t, FuncTy):
        argTys = [apply(s, a) for a in t.argTys]
        retTy = apply(s, t.retTy)
        return FuncTy(argTys, retTy)
    elif isinstance(t, VarTy):
        return s.get(t.s, t)

def applyList(s, xs):
    return [(apply(s, x), apply(s, y)) for x, y in xs]

def unify(x, y):
    if isinstance(x, AppTy) and isinstance(y, AppTy):
        s1 = unify(x.a, y.a)
        s2 = unify(apply(s1, x.b), apply(s1, y.b))
        return compose(s2, s1)
    elif isinstance(x, ConstructorTy) and isinstance(y, ConstructorTy) and (x == y):
        return empty()
    elif isinstance(x, FuncTy) and isinstance(y, FuncTy):
        if (len(x.argTys) != len(y.argTys)):
            return Exception("Wrong number of arguments")
        s1 = solve(zip(x.argTys, y.argTys))
        s2 = unify(apply(s1, x.retTy), apply(s1, y.retTy))
        return compose(s2, s1)
    elif isinstance(x, VarTy):
        return bind(x.s, y)
    elif isinstance(y, VarTy):
        return bind(y.s, x)
    else:
        raise InferError

def solve(xs):
    mgu = empty()
    cs = deque(xs)
    while len(cs):
        (a, b) = cs.pop()
        s = unify(a, b)
        mgu = compose(s, mgu)
        cs = deque(applyList(s, cs))
    return mgu

def bind(n, x):
    if x == n:
        return empty()
    elif occurs_check(n, x):
        raise Exception("InfiniteType") #InfiniteType(n, x)
    else:
        return dict([(n, x)])

def occurs_check(n, x):
    return n in ftv(x)

def union(s1, s2):
    nenv = s1.copy()
    nenv.update(s2)
    return nenv

def compose(s1, s2):
    s3 = dict((t, apply(s1, u)) for t, u in s2.items())
    return union(s1, s3)

class UnderDeteremined(Exception):
    def __str__(self):
        return "The types in the function are not fully determined by the \
                input types. Add annotations."

class InferError(Exception):
    def __init__(self, ty1, ty2):
        self.ty1 = ty1
        self.ty2 = ty2

    def __str__(self):
        return '\n'.join([
            "Type mismatch: ",
            "Given: ", "\t" + str(self.ty1),
            "Expected: ", "\t" + str(self.ty2)
        ])