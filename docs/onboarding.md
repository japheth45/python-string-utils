# Onboarding Notes

These notes record what has been verified about this repository. Claims below are confirmed against the source unless marked otherwise.

## What this library is

`python-string-utils` is a small Python library for validating, manipulating, and generating strings. Everything public is importable from the top-level package: `string_utils/__init__.py` re-exports the API from the submodules, so `from string_utils import slugify` works.

## Map of the package

- `string_utils/validation.py` holds the checking functions (`is_string`, `is_url`, `is_email`, `is_slug`, and others). They return booleans.
- `string_utils/manipulation.py` holds the transformation functions (`slugify`, `asciify`, `prettify`, `booleanize`, and others).
- `string_utils/generation.py` holds generators (`uuid`, `random_string`, and others).
- `string_utils/errors.py` defines `InvalidInputError`, the library's error for non-string input. It subclasses `TypeError`, and its message has the form `Expected "str", received "<type>"`.
- `string_utils/_regex.py` holds the compiled regular expressions the other modules share. The leading underscore marks it internal: patterns are used through the public functions, not imported by callers.

## Tests

Tests live in `tests/`, one file per public function. The full suite runs with `python -m unittest` and passes 407 tests at the verified baseline. A single function's tests run with `python -m unittest tests.test_slugify`.

## One behavior traced end to end: slugify

`slugify(input_string, separator='-')` was traced through the source and verified in a live session:

1. The input is validated with `is_string`; non-string input raises `InvalidInputError`.
2. The input is lowercased, and every run of characters that is not a letter or number is replaced with spaces (`NO_LETTERS_OR_NUMBERS_RE`), then the result is stripped.
3. Spaces are replaced with the separator (`SPACES_RE`), joining the tokens.
4. Consecutive separators are collapsed to one.
5. The result is converted to plain ASCII by `asciify`, so accented characters are transliterated.

## Documentation

`docs/` contains Sphinx pages that publish the public docstrings with `automodule`. A function's docstring is therefore part of its published contract: when behavior changes, the docstring changes with it.

## Likely inferences (not fully verified)

- Test organization appears complete for the public API, but coverage of edge cases has not been audited.
- The build and release scripts reflect practices from the time the project was last released; they have not been exercised here.
