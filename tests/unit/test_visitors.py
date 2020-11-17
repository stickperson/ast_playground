import ast
from unittest import mock

from surveyor.visitors import BaseClassVisitor, ImportFromVisitor


class TestBaseClassVisitor:
    BASE_CLASS_NAME = 'base'
    CLASS_NAME = 'implement'

    def run_class_def(self, expected_result, base_id=None, base_spec=None):
        if base_id is None:
            base_id = self.BASE_CLASS_NAME

        visitor = BaseClassVisitor(self.BASE_CLASS_NAME)
        node = mock.MagicMock()
        base = mock.Mock(spec=base_spec)
        base.configure_mock(id=base_id)
        node.configure_mock(name=self.CLASS_NAME, bases=[base])

        visitor.visit_ClassDef(node)
        assert visitor.classes == expected_result

    def test_visit_class_def(self):
        self.run_class_def({self.CLASS_NAME}, base_spec=ast.Name)

    def test_visit_class_def_incorrect_base(self):
        self.run_class_def(set())

    def test_visit_class_def_no_match(self):
        self.run_class_def(set(), base_id='bad', base_spec=ast.Name)


class TestImportFromVisitor:
    def test_visit_import_from(self):
        target = 'test'
        visitor = ImportFromVisitor([target])
        node = mock.MagicMock()
        name_mock = mock.Mock()
        name_mock.configure_mock(name=target)
        node.configure_mock(names=[name_mock])
        visitor.visit_ImportFrom(node)
        assert visitor.contains_target

    def test_visit_import_from_no_match(self):
        visitor = ImportFromVisitor(['hello'])
        node = mock.MagicMock()
        name_mock = mock.Mock()
        name_mock.configure_mock(name='bye')
        node.configure_mock(names=[name_mock])
        visitor.visit_ImportFrom(node)
        assert not visitor.contains_target
