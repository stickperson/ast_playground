Playing around with python's [ast](https://docs.python.org/3.8/library/ast.html) module to determine which tests to run when files change. Some of the code is inspired by [flake8](https://github.com/PyCQA/flake8).

Use case: you only want to run certain tests (here, integration tests) when a file changes. If you have 100 integration tests and the changes only affect one test, why run the other 99? The following strategy is employed here:
- TODO: pass in a list of changed files
- construct ast
- use `BaseClassVisitor` which inspects changed files for classes which implement a specific base class and keeps track of classnames
- look for all integration tests that import that classname
- load and run test suite

Future work:
- run tests in parallel
- possibly only run tests if the class itself changed, not just other code in the file
- remove hard-coded assumptions (though this is just a proof of concept and may be fine)
