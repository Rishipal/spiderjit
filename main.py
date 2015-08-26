__author__ = 'sarangis'

from ir.module import *
from ir.context import *
from ir.irbuilder import *
from ir.constants import *
from optimizer.passmanager import *
from optimizer.basicpass import *

int32Ty = IntType(32)
floatTy = FloatType()

def main():
    ctx = Context()
    mod = Module("MyModule", ctx)
    irbuilder = IRBuilder(mod, ctx)

    ft = irbuilder.create_function_type(int32Ty, floatTy, floatTy)
    f = irbuilder.create_function("test_fn", ft)

    ft1 = irbuilder.create_function_type(int32Ty, int32Ty, int32Ty)
    f1 = irbuilder.create_function("foo", ft1)

    arg0 = Argument(floatTy, "myarg")
    arg1 = Argument(floatTy, "myarg1")
    f.args = [arg0, arg1]

    arg2 = Argument(int32Ty, "a")
    arg3 = Argument(int32Ty, "b")
    f1.args = [arg2, arg3]

    bb = irbuilder.create_basic_block("entry", f)
    f.basic_blocks.append(bb)
    bb_exit = irbuilder.create_basic_block("exit", f)
    f.basic_blocks.append(bb_exit)

    irbuilder.insert_after(bb)
    irbuilder.create_call(f1, IntConstant(32, 5), IntConstant(32, 3))
    irbuilder.create_call(f1, IntConstant(32, 7), IntConstant(32, 2), name="call")
    irbuilder.create_call(f1, IntConstant(32, 9), IntConstant(32, 1), name="call")
    irbuilder.create_fadd(IntConstant(32, 4), IntConstant(32, 7))
    irbuilder.create_mul(IntConstant(32, 3), IntConstant(32, 9), name="mymul")
    irbuilder.create_mul(IntConstant(32, 6), IntConstant(32, 5), name="mymul")
    irbuilder.create_branch(bb_exit)

    irbuilder.insert_after(bb_exit)
    irbuilder.create_return()

    mod.functions.append(f)
    mod.functions.append(f1)
    print(mod)
    mod.validate()

    print("Running Passmanager:")
    print("-" * 50)
    passmgr = PassManager()
    passmgr.add_module_pass(PrintFunctionsPass())
    passmgr.add_function_pass(PrintBasicBlocksPass())
    passmgr.run(mod)

if __name__ == "__main__":
    main()