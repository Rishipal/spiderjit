__author__ = 'sarangis'

from pyjit.nodes import *
from collections import defaultdict
from utils.base_visitor import *

from ir.context import *
from ir.module import *
from ir.irbuilder import *
from ir.types import *
from ir.constants import *

int32Ty = IntType(32)
floatTy = FloatType()

class IREmitter(BaseVisitor):
    def __init__(self, mod_name):
        self.__ctx = Context()
        self.__module = Module(mod_name, self.__ctx)
        self.__irbuilder = IRBuilder(self.__module, self.__ctx)

    @property
    def irbuilder(self):
        return self.__irbuilder

    @property
    def module(self):
        return self.__module

    def visit_func(self, node):
        print(dir(node))
        irbuilder = self.irbuilder
        module = self.module
        ft = self.irbuilder.create_function_type(int32Ty, floatTy, floatTy)
        f = self.irbuilder.create_function(node.fname, ft)

        print(dir(node.args))
        f.args = [Argument(floatTy, arg) for arg in node.args]

        bb = irbuilder.create_basic_block("entry", f)
        f.basic_blocks.append(bb)
        bb_exit = irbuilder.create_basic_block("exit", f)
        f.basic_blocks.append(bb_exit)

        irbuilder.insert_after(bb)
        irbuilder.create_fadd(IntConstant(32, 4), IntConstant(32, 7))
        irbuilder.create_mul(IntConstant(32, 3), IntConstant(32, 9), name="mymul")
        irbuilder.create_mul(IntConstant(32, 6), IntConstant(32, 5), name="mymul")
        irbuilder.create_branch(bb_exit)

        irbuilder.insert_after(bb_exit)
        irbuilder.create_return()

        module.functions.append(f)
        print(module)
        module.validate()
