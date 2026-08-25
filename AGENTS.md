# Repository Guidance

## Purpose

This repository provides a Python library for validating, manipulating, and generating strings. Callers use the public API exposed by the `string_utils` package.

## Layout

- Production source lives in `string_utils/`: `validation.py` (checks), `manipulation.py` (transformations), `generation.py` (generators), `errors.py` (library errors), and `_regex.py` (compiled patterns for internal use only).
- Tests live in `tests/`, one file per public function (for example, `tests/test_slugify.py`).
- Documentation lives in `docs/` and uses Sphinx `automodule` pages, so public docstrings are published as API documentation.
- `docs/onboarding.md` and `PROJECT_STATUS.md` record what the team has verified about this repository and the current state of work.

## Commands

- Run the full test suite with `python -m unittest`.
- Run one function's tests with `python -m unittest tests.test_slugify` (substitute the file for the function you are working on).

## Working agreements

- Read the current ticket, the relevant source, and the focused tests before proposing any change.
- When a task is ambiguous, ask clarifying questions and propose a plan before editing anything.
- Keep every change tied to the current ticket and small enough to review line by line.
- Do not add dependencies, modernize tooling, rename files, or perform cleanup outside the agreed scope.
- Stop and ask before changing any file outside the approved scope for the current task.
- Do not remove or weaken tests to make a failing check pass.
- Report commands and observed results rather than unsupported summaries.

## Definition of done

Work is ready for review only when the open decisions are recorded, the approved plan was followed, every changed file belongs to the task, the relevant checks were run with results recorded, the diff has been read, and remaining risks are written down.
