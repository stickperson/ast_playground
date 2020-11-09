import ast
from typing import List


class BaseClassVisitor(ast.NodeVisitor):
    """
    Maintains a set of classes that inherit from base_class_name
    """
    def __init__(self, base_class_name: str) -> None:
        super().__init__()
        self._base_class_name = base_class_name
        self.classes = set()

    def visit_ClassDef(self, node: ast.Call) -> None:
        """
        Checks if the the node inherits from self._base_class_name.

        Note: currently, this only works if the base class is imported directly. E.g.
        from mycode.base import BaseClass
        class MyClass(BaseClass):
            ...

        would work while

        from mycode import base
        class MyClass(base.BaseClass):
            ...

        would not. Depending on how the class was imported (and maybe even if it is aliased), the instance of base in
        node.bases will differ.
        """
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id == self._base_class_name:
                self.classes.add(node.name)
        self.generic_visit(node)


class ImportFromVisitor(ast.NodeVisitor):
    def __init__(self, targets: List[str]) -> None:
        super().__init__()

        self._targets = targets
        self.contains_target = False

    def visit_ImportFrom(self, node: ast.Call) -> None:
        for name in node.names:
            if name.name in self._targets:
                self.contains_target = True

        self.generic_visit(node)
