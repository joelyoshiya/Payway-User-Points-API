# Running Unit-tests with a typical directory structure

See [This link](https://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure)

Basically use unittest [cli](https://docs.python.org/2/library/unittest.html#command-line-interface) and make the files you want to test into packages. Then important them in the tester file.

```txt
new_project
├── antigravity
│   ├── __init__.py         # make it a package
│   └── antigravity.py
└── test
    ├── __init__.py         # also make test a package
    └── test_antigravity.py

```

## Run Tests

To run the test:

```txt
cd python_solution
python -m unittest test.test
```
