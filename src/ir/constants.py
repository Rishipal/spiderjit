__author__ = 'sarangis'

from ir.value import *

class Constant(Value):
    def __init__(self):
        Value.__init__(self)

    def __str__(self):
        pass

    __repr__ = __str__

class IntConstant(Constant):
    def __init__(self, bits, initializer):
        Constant.__init__(self)
        self.__type = IntType(bits)
        self.__initializer = initializer

    def __str__(self):
        return str(self.__type) + " " + str(self.__initializer)

    @property
    def type(self):
        return self.__type

class FloatConstant(Constant):
    def __init__(self, initializer):
        Constant.__init__(self)
        self.__initializer = initializer

    @property
    def type(self):
        return self.__type

    def __str__(self):
        return str(self.__type) + " " + str(self.__initializer)


class DoubleConstant(Constant):
    def __init__(self, initializer):
        Constant.__init__(self)
        self.__initializer = initializer

    @property
    def type(self):
        return self.__type

    def __str__(self):
        return str(self.__type) + " " + str(self.__initializer)


class StrConstant(Constant):
    def __init__(self):
        Constant.__init__(self)

    @property
    def type(self):
        return self.__type

    def __str__(self):
        return ""