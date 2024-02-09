# Pylint Boolean Naming Checker

This is a [pylint](https://pylint.readthedocs.io/en/stable/) Checker to enforce variables with boolean results include common phrases implying True/False states.

<details>
    <summary>Inspiration taken from here</summary>

    Came across this [issue](https://github.com/pylint-dev/pylint/issues/9409) and thought it would be cool to try and do it myself.
</details>

## How to Use

Install the package and then add it to the pylint runtime plugins.

```bash
# assuming git cloning until PyPI publish
git clone ...
cd pylint-boolean-naming
pip install .

# inside your code base
pylint --load-plugins pylint-boolean-naming \
    ... # other commands
```

## Code Quality

Use [pre-commit](https://pre-commit.com) for general code quality and as a CI checker. This has hooks for:
    - [MyPy](https://mypy.readthedocs.io/en/stable/)
    - [Ruff](https://astral.sh/ruff)
    - [Poetry](https://python-poetry.org/)

## Contributing

We welcome all forms of contributions such as updates for documentation, new code, checking issues for duplicates or telling us that we can close them, confirming that issues still exist, creating issues because you found a bug or want a feature, etc. Everything is much appreciated!
