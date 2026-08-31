# Project Status

This file is the running record of work on this repository. It records the verified baseline, recent work, and open questions. Update it whenever the state of the repository changes.

## Verified baseline (from onboarding)

- Git status at baseline: working tree clean.
- Python: 3.14 (project-managed environment).
- Test command: `python -m unittest`
- Result: 407 tests, OK.

## Recent work

- Onboarding review completed. Repository structure, entry points, and the `slugify` pipeline were traced and verified against the source. Findings are recorded in `docs/onboarding.md`.
- Repository guidance for assisted development was added in `AGENTS.md`.
- Ticket SUTIL-101 fixed. Details below.

## SUTIL-101 — slugify separator validation (fixed)

- What changed and why: `slugify` accepted any value for its `separator` argument and then crashed inside the regular-expression or codec machinery with errors that never mentioned the separator. Per the agreed behavior, a non-string separator now raises the library's `InvalidInputError`, the same way a bad first argument does, and an empty-string separator raises `ValueError` with the message `separator must be a non-empty string`. All previously valid calls behave exactly as before, the default separator remains `'-'`, and the `slugify` docstring states the new rule.
- Files changed: `string_utils/manipulation.py`, `tests/test_slugify.py`.
- Commands run and observed results:
  - `python -m unittest` (before the change): Ran 407 tests — OK.
  - `python -m unittest tests.test_slugify` (new tests added, fix not yet applied): Ran 10 tests — FAILED (failures=1, errors=1). The two new tests were seen failing.
  - `python -m unittest tests.test_slugify` (after the fix): Ran 10 tests — OK.
  - `python -m unittest` (after the fix): Ran 409 tests — OK.
  - Reproduction, before: `python -c "from string_utils import slugify; print(slugify('hello world', separator=''))"` ended with `re.PatternError: nothing to repeat at position 0`. After: the same command ends with `ValueError: separator must be a non-empty string`.
- Not claimed: this change has not been reviewed beyond this record, and it has not been verified for release.

## Unresolved questions

- `tox.ini` and `.travis.yml` list Python 3.5 through 3.8, but the environment runs a much newer Python and the suite passes. The project's supported-version policy is unconfirmed.
- Release and packaging practice is unconfirmed: `setup.py` and `build.sh` exist, but current release steps have not been verified with a maintainer.
- SUTIL-101 restricted which separator values `slugify` accepts, but only the default and common single-character separators were exercised by the new tests. Nothing in the documentation limits the separator to one character, and no check was made of how other functions in this library that deal with slugs handle less common separator values.
