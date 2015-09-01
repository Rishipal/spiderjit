class BaseVisitor(object):
    def __init__(self):
        pass

    def visit(self, node):
        name = "visit_%s" % type(node).__name__.lower()
        if hasattr(self, name):
            return getattr(self, name)(node)
        else:
            return self.generic_visit(node)

    def generic_visit(self, node):
        raise NotImplementedError("Visitor class doesn't implement visit_%s" % type(node).__name__)
