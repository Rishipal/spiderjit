__author__ = 'sarangis'

import sys
import ast
import types
import ctypes
import inspect
import pprint
import string
import numpy as np

from textwrap import dedent
from collections import deque, defaultdict

from pyjit.nodes import *

primops = {ast.Add: "add#", ast.Mult: "mult#"}

class PythonVisitor(ast.NodeVisitor):

    def __init__(self):
        pass

    def __call__(self, source):
        if isinstance(source, types.ModuleType):
            source = dedent(inspect.getsource(source))
        if isinstance(source, types.FunctionType):
            source = dedent(inspect.getsource(source))
        if isinstance(source, types.LambdaType):
            source = dedent(inspect.getsource(source))
        elif isinstance(source, str):
            source = dedent(source)
        else:
            raise NotImplementedError

        self._source = source
        self._ast = ast.parse(source)
        return self.visit(self._ast)

    def visit_Module(self, node):
        body = [self.visit(n) for n in node.body]
        return body[0]

    def visit_Name(self, node):
        return Var(node.id)

    def visit_Num(self, node):
        if isinstance(node.n, float):
            return LitFloat(node.n)
        else:
            return LitInt(node.n)

    def visit_Bool(self, node):
        return LitBool(node.n)

    def visit_Call(self, node):
        name = self.visit(node.func)
        args = map(self.visit, node.args)
        keywords = map(self.visit, node.keywords)
        return App(name, args)

    def visit_BinOp(self, node):
        op_str = node.op.__class__
        a = self.visit(node.left)
        b = self.visit(node.right)
        opname = primops[op_str]
        return Prim(opname, [a, b])

    def visit_Assign(self, node):
        targets = node.targets

        assert len(node.targets) == 1
        var = node.targets[0].id
        val = self.visit(node.value)
        return Assign(var, val)

    def visit_FunctionDef(self, node):
        stmts = list(node.body)
        stmts = [self.visit(stmt) for stmt in stmts]
        args = [self.visit(arg) for arg in node.args.args]
        res = Func(node.name, args, stmts)
        return res

    def visit_arg(self, node):
        return Var(node.arg)

    def visit_Pass(self, node):
        return Noop()

    def visit_Lambda(self, node):
        args = self.visit(node.args)
        body = self.visit(node.body)

    def visit_Return(self, node):
        val = self.visit(node.value)
        return Return(val)

    def visit_Attribute(self, node):
        if node.attr == "shape":
            val = self.visit(node.value)
            return Prim("shape#", [val])
        else:
            raise NotImplementedError

    def visit_Subscript(self, node):
        if isinstance(node.ctx, ast.Load):
            if node.slice:
                val = self.visit(node.value)
                ix = self.visit(node.slice.value)
                return Index(val, ix)
        elif isinstance(node.ctx, ast.Store):
            raise NotImplementedError

    def visit_For(self, node):
        target = self.visit(node.target)
        stmts = [self.visit(stmt) for stmt in node.body]
        if node.iter.func.id in {"xrange", "range"}:
            args = [self.visit(arg) for arg in node.iter.args]
        else:
            raise Exception("Loop must be over range")

        if len(args) == 1:   # xrange(n)
            return Loop(target, LitInt(0, type=int32), args[0], stmts)
        elif len(args) == 2:  # xrange(n,m)
            return Loop(target, args[0], args[1], stmts)

    def visit_AugAssign(self, node):
        if isinstance(node.op, ast.Add):
            ref = node.target.id
            value = self.visit(node.value)
            return Assign(ref, Prim("add#", [Var(ref), value]))
        if isinstance(node.op, ast.Mul):
            ref = node.target.id
            value = self.visit(node.value)
            return Assign(ref, Prim("mult#", [Var(ref), value]))
        else:
            raise NotImplementedError

    def generic_visit(self, node):
        raise NotImplementedError