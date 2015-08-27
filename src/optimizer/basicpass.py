__author__ = 'sarangis'

from optimizer.pass_support import *
from ir.validator import *
from ir.module import *
from ir.function import *

class PrintFunctionsPass(ModulePass):
    def __init__(self):
        pass

    @verify(node=Module)
    def run_on_module(self, node):
        print()
        print("Functions List:")
        print("-" * 50)
        for f in node.functions:
            print(f.name)


class PrintBasicBlocksPass(FunctionPass):
    def __init__(self):
        pass

    @verify(node=Function)
    def run_on_function(self, node):
        print()
        print("Function: %s" % node.name)
        print("Basic Block List:")
        print("-" * 50)
        for bb in node.basic_blocks:
            print(bb.name)