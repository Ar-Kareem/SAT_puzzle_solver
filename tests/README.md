# Testing

First, make sure the environment is created, activated, and the dependencies are installed.

```bash
conda create -p ./env python=3.11
conda activate ./env
pip install -r requirements.txt -r requirements-dev.txt
```

You can run almost all of the tests by running:

```bash
pytest
```

This will still skip the slow and very slow tests. To run the slow tests `pytest -m "slow and very_slow"` or for everything `pytest -m "not asdf"`.

You can run a specific set of tests by running:

```bash
pytest -k binairo -n 0 -s
```

This will run tests with `binairo` in the name without multithreading (`-n 0`) and with showing the output (`-s`).

Or you can run a test module by running:

```bash
python -m tests.test_binairo
```

Although this will run the `__main__` block of the test module and thus might be missing some tests and will also terminate after the first failure.