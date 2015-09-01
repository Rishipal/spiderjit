from utils.base_visitor import BaseVisitor

class VirtualMachine(BaseVisitor):
    def __init__(self):
        pass

    def visit_module(self):
        pass

    def visit_function(self):
        pass

    def visit_callinstruction(self):
        pass

    def visit_terminateinstruction(self):
        pass

    def visit_returninstruction(self):
        pass

    def visit_selectinstruction(self):
        pass

    def visit_loadinstruction(self):
        pass

    def visit_storeinstruction(self):
        pass

    def visit_addinstruction(self):
        pass
    
    def visit_subinstruction(self):
        pass

    def visit_mulinstruction(self):
        pass

    def visit_divinstruction(self):
        pass

    def visit_faddinstruction(self):
        pass

    def visit_fsubinstruction(self):
        pass

    def visit_fmulinstruction(self):
        pass

    def visit_fdivinstruction(self):
        pass

    def visit_allocainstruction(self):
        pass

    def visit_phiinstruction(self):
        pass

    def visit_branchinstruction(self):
        pass