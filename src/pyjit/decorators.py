__author__ = 'sarangis'

from pyjit.visitors import *
from pyjit.type_infer import *
from pyjit.codegen import *
import numpy as np

def arg_pytype(arg):
    if isinstance(arg, np.ndarray):
        if arg.dtype == np.dtype('int32'):
            return array(int32)
        elif arg.dtype == np.dtype('int64'):
            return array(int64)
        elif arg.dtype == np.dtype('double'):
            return array(double64)
        elif arg.dtype == np.dtype('float'):
            return array(float32)
    elif isinstance(arg, int) & (arg < sys.maxint):
        return int64
    elif isinstance(arg, float):
        return double64
    else:
        raise Exception("Type not supported: %s" % type(arg))

def specialize(ast, infer_ty, mgu):
    def _wrapper(*args):
        return None
        # types = map(arg_pytype, list(args))
        # spec_ty = TFun(argtys=types, retty=TVar("$retty"))
        # unifier = unify(infer_ty, spec_ty)
        # specializer = compose(unifier, mgu)
        #
        # retty = apply(specializer, TVar("$retty"))
        # argtys = [apply(specializer, ty) for ty in types]
        # print('Specialized Function:', TFun(argtys, retty))
        #
        # if determined(retty) and all(map(determined, argtys)):
        #     key = mangler(ast.fname, argtys)
        #     # Don't recompile after we've specialized.
        #     if key in function_cache:
        #         return function_cache[key](*args)
        #     else:
        #         llfunc = codegen(ast, specializer, retty, argtys)
        #         pyfunc = wrap_module(argtys, llfunc)
        #         function_cache[key] = pyfunc
        #         return pyfunc(*args)
        # else:
        #     raise UnderDeteremined()
    return _wrapper

def autojit(fn):
    transformer = PythonVisitor()
    ast = transformer(fn)
    (ty, mgu) = typeinfer(ast)
    return specialize(ast, ty, mgu)

def typeinfer(ast):
    infer = InferType()
    sig = infer.visit(ast)

    print('Signature:%s \n' % sig)

    print('Constraints:')
    for (a,b) in infer.constraints:
        print(a, '~', b)

    # mgu = solve(infer.constraints)
    TypeSolver.solve(infer.constraints)
    # infer_ty = apply(mgu, sig)
    # return (infer_ty, mgu)
    return (None, None)

def codegen(ast, specializer, retty, argtys):
    cgen = IREmitter(specializer, retty, argtys)
    mod = cgen.visit(ast)
    cgen.function.verify()
    print(cgen.function)
    # print(module.to_native_assembly())
    return cgen.function