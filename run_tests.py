import ast
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
    def __init__(self, start_directory='./tests', pattern='integration*'):
        self._start_directory = start_directory
        self._pattern = pattern
        self._inspector_cls = Inspector
        self._loader_cls = unittest.TestLoader
        self._test_suite_cls = unittest.TestSuite

        self._inspector = None
        self._loader = None
        self._test_suite = None
        self._test_filenames = set()

    def initialize(self):
        self.make_inspector()
        self.make_loader()
        self.make_test_suite()

    def make_inspector(self):
        self._inspector = Inspector('./mycode/thing.py')

    def make_loader(self):
        self._loader = self._loader_cls()

    def make_test_suite(self):
        self._test_suite = self._test_suite_cls()

    def run(self):
        self.initialize()
        self.make_inspector()
        self.make_loader()
        self.make_test_suite()

        self.run_inspector()
        self.find_matches()
        self.setup_tests()
        self.run_tests()

    def run_inspector(self):
        self._inspector.inspect()

    def run_tests(self):
        unittest.installHandler()
        runner = unittest.TextTestRunner()
        runner.run(self._test_suite)

    def find_matches(self):
        targets = self._inspector.report()
        for root, subdirs, files in os.walk('./tests'):
            for f in files:
                if f.startswith('integration_') and f.endswith('.py'):
                    full_path = os.path.join(root, f)
                    tree = ast.parse(open(full_path).read())
                    visitor = ImportFromVisitor(list(targets))
                    visitor.visit(tree)
                    if visitor.contains_target:
                        self._test_filenames.add((root, f))

    def setup_tests(self):
        for root, fname in self._test_filenames:
            module = self._loader.discover(root, fname)
            if module and module.countTestCases():
                self._test_suite.addTests(module)


if __name__ == '__main__':
    app = Application()
    app.run()
