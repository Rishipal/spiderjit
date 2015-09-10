__author__ = 'sarangis'

from optimizer.passmanager import *
from optimizer.basicpass import *
from pyjit.decorators import *
from vm.vm import *
from ir.interpreter import *
from pytests.fib import *

int32Ty = IntType(32)
floatTy = FloatType()

def generate_ir():
    ctx = Context()
    mod = Module("MyModule", ctx)
    irbuilder = IRBuilder(mod, ctx)

    irbuilder.create_global("first_global", IntConstant(32, 4))
    irbuilder.create_global("second_global", IntConstant(32, 9))

    # Create the fibonacci function
    ft1 = irbuilder.create_function_type(int32Ty, int32Ty)
    irfib = irbuilder.create_function("fib", ft1)
    n_arg = Argument(int32Ty, "n")
    irfib.args = [n_arg]

    entry_bb = irbuilder.create_basic_block("entry", irfib)
    irfib.basic_blocks.append(entry_bb)
    irbuilder.insert_after(entry_bb)
    # Now add a icmp instruction
    icmp = irbuilder.create_icmp(n_arg, IntConstant(32, 1))
    ifcont = irbuilder.create_basic_block("if-cont", irfib)
    thenblock = irbuilder.create_basic_block("then", irfib)
    irbuilder.create_cond_branch(icmp, True, ifcont, thenblock)
    irfib.basic_blocks.append(ifcont)
    irfib.basic_blocks.append(thenblock)

    irbuilder.insert_after(ifcont)
    irbuilder.create_or(IntConstant(32, 15), IntConstant(32, 11))
    irbuilder.create_return(IntConstant(32, 1))

    irbuilder.insert_after(thenblock)
    n_minus_1 = irbuilder.create_sub(n_arg, IntConstant(32, 1))
    n_minus_2 = irbuilder.create_sub(n_arg, IntConstant(32, 2))
    call1 = irbuilder.create_call(irfib, n_minus_1)
    call2 = irbuilder.create_call(irfib, n_minus_2)
    final_res = irbuilder.create_add(call1, call2)
    irbuilder.create_return(final_res)

    # Create the main entry point
    ft = irbuilder.create_function_type(int32Ty)
    f = irbuilder.create_function("main", ft)
    bb = irbuilder.create_basic_block("entry", f)
    f.basic_blocks.append(bb)

    irbuilder.insert_after(bb)
    call_fib = irbuilder.create_call(irfib, IntConstant(32, 9))
    irbuilder.create_return(call_fib)

    mod.functions.append(f)
    mod.functions.append(irfib)
    print("-" * 100)
    print(mod)
    mod.validate()

    mod.entry_point = f

    print("Running Passmanager:")
    print("-" * 50)
    passmgr = PassManager()
    # passmgr.add_module_pass(PrintFunctionsPass())
    # passmgr.add_function_pass(PrintBasicBlocksPass())
    # passmgr.add_function_pass(PrintInstructionUsesPass())
    passmgr.add_function_pass(DominatorTreeAnalysisPass())
    passmgr.run(mod)

    print("-" * 50)
    print("Running IR Virtual machine")
    irvm = IRVirtualMachine()
    irvm.visit(mod)
    print(irvm.eval_result)

# @autojit
# def addup(n):
#     x = 1
#     for i in range(n):
#         n += 1 + x
#     return n

#@autojit
#def add(a, b):
#    c = a + b
#    return c

# @autojit
# def addone(a):
#     return a + 1

#@autojit
#def addstring(one, two):
#    two = two + "testx"
#    return "hello" + one + two

# @autojit
# def test_conditional():
#     var = 1
#     if var <= 2:
#         var = []
#     elif var == 3:
#         var = {}
#     else:
#         var = 'hi'

def test_bytecode_vm():
    dis.dis(fib.__code__)
    for n in range(10):
        vm = BytecodeVM(fib, n)
        vm.execute()
        print("fib(", n, ") =", fib(n), " = ", vm.value)

    #vm = BytecodeVM(fib, 3)
    #vm.execute()
    #print(vm.value)

if __name__ == "__main__":
    # generate_ir()
    test_bytecode_vm()
    generate_ir()
