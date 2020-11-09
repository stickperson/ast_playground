from unittest import mock
import pytest
from run_tests import Inspector


class TestInspector:
    @mock.patch('run_tests.BaseClassVisitor')
    @mock.patch('ast.parse')
    def test_inspect(self, ast_mock, base_mock, tmp_path):
        instance = base_mock.return_value
        d = tmp_path / 'test'
        d.mkdir()
        f = d / 'test'
        f.write_text('hello')
        inspector = Inspector(f)
        inspector.inspect()
        assert instance.visit.called_once

    def test_report(self):
        inspector = Inspector('test')
        inspector._visitor = mock.Mock()
        inspector._visitor.classes = 1
        assert inspector.report() == 1

    def test_report_raises_assertion(self):
        inspector = Inspector('test')
        with pytest.raises(AssertionError):
            inspector.report()
