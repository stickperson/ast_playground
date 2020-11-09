import ast
from visitors import BaseClassVisitor


class TestBaseClassVisitor:
    code = '''\
class BaseClass:
    pass

class Direct(BaseClass):
    pass

class Indirect(Direct):
    pass
    '''

    def test_direct_inheritance(self):
        tree = ast.parse(self.code)
        visitor = BaseClassVisitor('BaseClass')
        visitor.visit(tree)
        assert len(visitor.classes) == 1
        assert visitor.classes == {'Direct'}

    def test_no_matches(self):
        tree = ast.parse(self.code)
        visitor = BaseClassVisitor('Missing')
        visitor.visit(tree)
        assert len(visitor.classes) == 0
