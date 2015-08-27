__author__ = 'sarangis'

from ir.exceptions import *
from ir.validator import *
from ir.context import *

class Module(Validator):
    @verify(name=str, ctx=Context)
    def __init__(self, name, ctx):
        self.__context = ctx
        self.__name = name
        self.__globals = []
        self.__functions = []
        self.__func_declarations = []
        self.__data_layout = []
        self.__target_arch = ""

    @property
    def globals(self):
        return self.__globals

    @globals.setter
    def globals(self, globalv):
        self.__globals.append(globalv)

    @property
    def functions(self):
        return self.__functions

    @functions.setter
    def functions(self, func):
        self.__functions.append(func)

    @property
    def function_decls(self, func_decl):
        self.__func_declarations.append(func_decl)

    @property
    def datalayout(self):
        return self.__data_layout

    @datalayout.setter
    def datalayout(self, dl):
        self.__data_layout = dl

    @property
    def target_arch(self):
        return self.__target_arch

    @target_arch.setter
    def target_arch(self, arch):
        self.__target_arch = arch

    @property
    def name(self):
        return self.__name

    @property
    def context(self):
        return self.__context

    def __str__(self):
        output_str = ""
        output_str += "Module: %s\n" % (self.__name)
        output_str += "Target Datalayout: %s\n" % (self.__data_layout)
        output_str += "Target Arch: %s\n" % (self.__target_arch)

        for f in self.__func_declarations:
            output_str += str(f)

        for f in self.__functions:
            output_str += str(f)

        return output_str

    def validate(self):
        for f in self.__functions:
            f.validate()

    __repr__ = __str__