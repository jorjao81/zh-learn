This file contains instructions for Gemini.

- Do not use libraries or frameworks that are not already in use.
- Mimic the style and structure of the existing code.
- Add comments only when necessary to explain complex logic.

## Project Conventions

- **Formatting:** This project uses `black` for code formatting. All code should be formatted with `black` before committing.
- **Linting:** This project uses `flake8` for linting. All code should pass `flake8` checks before committing.
- **Type Checking:** This project uses `mypy` for static type checking. All code should pass `mypy` checks before committing.

## Pre-commit Hooks

This project uses `pre-commit` to enforce code quality. Before committing any changes, please run `pre-commit run --all-files` to ensure that all checks pass.