import ast
from fnmatch import fnmatch
import os
import unittest

from visitors import BaseClassVisitor, ImportFromVisitor


class Inspector:
    """
    Looks at a file, returns a list of class names that inherit from Workflow class
    """
    def __init__(self, fname):
        self._fname = fname
        self._visitor = None

    def inspect(self):
        tree = ast.parse(open(self._fname).read())
        self._visitor = BaseClassVisitor('Workflow')
        self._visitor.visit(tree)

    def report(self):
        assert self._visitor is not None, 'Inspect must be run before calling report()'
        return self._visitor.classes


class Application:
    def __init__(self, changed_files, start_directory='./tests', pattern='integration*.py'):
        self._changed_files = changed_files
        self._start_directory = start_directory
        self._pattern = pattern
        self._inspector_cls = Inspector
        self._loader_cls = unittest.TestLoader
        self._test_suite_cls = unittest.TestSuite

        self._inspectors = []
        self._loader = None
        self._test_suite = None
        self._test_filenames = set()

    def _find_matches(self):
        """
        Retrieves target classes from the inspector and inspects test files for
        imports of those classnames
        """
        targets = set()
        for inspector in self._inspectors:
            targets.update(inspector.report())

        for root, subdirs, files in os.walk(self._start_directory):
            for f in files:
                if fnmatch(f, self._pattern):
                    full_path = os.path.join(root, f)
                    tree = ast.parse(open(full_path).read())
                    visitor = ImportFromVisitor(list(targets))
                    visitor.visit(tree)
                    if visitor.contains_target:
                        self._test_filenames.add((root, f))

    def initialize(self):
        self.make_inspectors()
        self.make_loader()
        self.make_test_suite()

    def make_inspectors(self):
        for f in self._changed_files:
            inspector = Inspector(f)
            self._inspectors.append(inspector)

    def make_loader(self):
        self._loader = self._loader_cls()

    def make_test_suite(self):
        self._test_suite = self._test_suite_cls()

    def run(self):
        self.initialize()

        self._run_inspectors()
        self._find_matches()
        self._setup_tests()
        self._run_tests()

    def _run_inspectors(self):
        for inspector in self._inspectors:
            inspector.inspect()

    def _run_tests(self):
        unittest.installHandler()
        runner = unittest.TextTestRunner()
        runner.run(self._test_suite)

    def _setup_tests(self):
        """
        Discovers and loads tests
        """
        for root, fname in self._test_filenames:
            module = self._loader.discover(root, fname)
            if module and module.countTestCases():
                self._test_suite.addTests(module)


if __name__ == '__main__':
    app = Application(['./mycode/thing.py'])
    app.run()
