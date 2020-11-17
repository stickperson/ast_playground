import argparse
import ast
import os
import subprocess
import sys
import unittest
from fnmatch import fnmatch
from typing import Any, List, Set, Tuple

from .visitors import BaseClassVisitor, ImportFromVisitor


class Inspector:
    """
    Looks at a file, returns a list of class names that inherit from Workflow class
    """
    def __init__(self, fname, base_class):
        self._fname = fname
        self._base_class = base_class
        self._visitor = None

    def inspect(self):
        tree = ast.parse(open(self._fname).read())
        self._visitor = BaseClassVisitor(self._base_class)
        self._visitor.visit(tree)

    def report(self):
        assert self._visitor is not None, 'Inspect must be run before calling report()'
        return self._visitor.classes


class Application:
    def __init__(
        self,
        changed_files: List[str],
        base_class: str,
        start_directory: str = './tests',
        pattern: str = 'integration*.py'
    ):
        self._changed_files = changed_files
        self._base_class = base_class
        self._start_directory = start_directory
        self._pattern = pattern
        self._inspector_cls = Inspector
        self._loader_cls = unittest.TestLoader
        self._test_suite_cls = unittest.TestSuite

        self._inspectors: List[Any] = []
        self._loader = None
        self._test_suite = None
        self._test_filenames: Set[Tuple[str, str]] = set()

    def _find_matches(self) -> None:
        """
        Retrieves target classes from the inspector and inspects test files for
        imports of those classnames
        """
        targets = set()
        for inspector in self._inspectors:
            targets.update(inspector.report())

        for root, _, files in os.walk(self._start_directory):
            for f in files:
                if fnmatch(f, self._pattern):
                    full_path = os.path.join(root, f)
                    tree = ast.parse(open(full_path).read())
                    visitor = ImportFromVisitor(list(targets))
                    visitor.visit(tree)
                    if visitor.contains_target:
                        self._test_filenames.add((root, f))

    def initialize(self) -> None:
        self.make_inspectors()
        self.make_loader()
        self.make_test_suite()

    def make_inspectors(self) -> None:
        for f in self._changed_files:
            inspector = Inspector(f, self._base_class)
            self._inspectors.append(inspector)

    def make_loader(self) -> None:
        self._loader = self._loader_cls()  # type: ignore

    def make_test_suite(self) -> None:
        self._test_suite = self._test_suite_cls()  # type: ignore

    def run(self) -> None:
        self.initialize()

        self._run_inspectors()
        self._find_matches()
        self._setup_tests()
        self._run_tests()

    def _run_inspectors(self) -> None:
        for inspector in self._inspectors:
            inspector.inspect()

    def _run_tests(self) -> None:
        unittest.installHandler()
        runner = unittest.TextTestRunner()
        runner.run(self._test_suite)  # type: ignore

    def _setup_tests(self) -> None:
        """
        Discovers and loads tests
        """
        for root, fname in self._test_filenames:
            module = self._loader.discover(root, fname)  # type: ignore
            if module and module.countTestCases():
                self._test_suite.addTests(module)  # type: ignore
        return


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('base_class', help='Name of the target base class')
    parser.add_argument('--files', nargs='+', default=None)
    parser.add_argument('--start-directory', default='.')
    parser.add_argument('--pattern', default='integration*.py')
    args = parser.parse_args()
    files = args.files
    if not files:
        cmd = ['git', 'diff', '--name-only', '@{1}']
        files = subprocess.check_output(cmd, encoding='utf8').split()
        print(files)
    app = Application(
        files, args.base_class, start_directory=args.start_directory, pattern=args.pattern
    )
    app.run()
    sys.exit(0)


if __name__ == '__main__':
    main()
    sys.exit(0)
