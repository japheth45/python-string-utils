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
- Ticket SUTIL-104 filed during release verification of SUTIL-101 and fixed. Details below.

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

## SUTIL-104 — is_slug rejects every slug built with a multi-character separator (ticket, filed during SUTIL-101 verification)

Project: SUTIL — string_utils library
Type: Bug | Priority: Medium | Status: Done | Assignee: Unassigned
Filed from: release verification of SUTIL-101
Affects version: 1.0.0 | Component: string_utils / validation
Labels: verification, round-trip

### Description

Round-trip verification of the SUTIL-101 fix showed that every slug `slugify` produces with a multi-character separator is rejected by `is_slug` when checked with the same separator. `slugify`'s output is correct per its documentation; the defect is in `is_slug`.

### Steps to reproduce

Each command was run from the repository root.

    python -c "from string_utils import slugify; print(repr(slugify('hello world', separator='..')))"

Observed output:

    'hello..world'

    python -c "from string_utils import is_slug; print(is_slug('hello..world', separator='..'))"

Observed output:

    False

The round-trip test matrix (five separators, three inputs, fifteen pairs) reports:

    Ran 1 test ...
    FAILED (failures=3)

All three failures are the pairs using the two-character separator; every single-character pair passes.

### Expected behavior

`is_slug` returns True for any slug `slugify` produces with the same separator. Inputs that `slugify` reduces to the empty string are excluded, because the empty string is not a slug.

### Actual behavior

Any separator longer than one character is rejected: `'..'`, `'--'`, `'__'`, and `'::'` are all confirmed. Single-character separators round-trip correctly.

### Evidence

In `string_utils/validation.py`, the pattern applies its `*?` quantifier to only the last character of the escaped separator, so a multi-character separator is never matched as a unit.

### Exposing tests

The exposing tests were committed with the fix as `tests/test_slugify_round_trip.py`, after being seen failing first (`Ran 1 test`, `FAILED (failures=3)`).

### Open decisions

1. Strings with consecutive separator runs (for example `'oh-----yeah'`) are currently accepted, and the existing test `test_slug_can_have_multiple_consecutive_separator_signs` pins that behavior. Must a corrected pattern preserve it?
2. `is_slug` crashes today when the separator is the empty string. Should it validate its separator the way `slugify` now does, or is that a separate follow-up ticket?
3. Does the `is_slug` docstring need a stated rule for the separator argument?

## SUTIL-104 — is_slug rejects slugs built with multi-character separators (fixed)

- What changed and why: `is_slug` built its pattern so that the repeat quantifier applied to the last character of the escaped separator only, so `is_slug('hello..world', '..')` returned False for a value `slugify` had just produced. The pattern now treats the whole separator as a unit: `^[a-z\d]+(?:(?:<sep>)+[a-z\d]+)*$`. Consecutive separators are still accepted, as the existing tests require.
- Files changed: `string_utils/validation.py`, `tests/test_slugify_round_trip.py` (new; the round-trip matrix from the SUTIL-104 ticket).
- Commands run and observed results: `python -m unittest tests.test_slugify_round_trip` before the fix: Ran 1 test — FAILED (failures=3), all naming the `'..'` separator. After the fix: Ran 1 test — OK. Full suite after the fix: Ran 410 tests — OK.
- Open decision recorded on the ticket: with this pattern an empty separator no longer raises inside `re`; `is_slug('hello', '')` quietly returns True, while `slugify` rejects an empty separator with `ValueError` since SUTIL-101. Whether `is_slug` should validate its separator the same way is not decided here.

## SUTIL-105 — modernization pass: bug fix, refactor, packaging (done, kept as three commits)

- What changed and why: SUTIL-105 asked for three kinds of change on the whole library, kept separate so the refactor can be reviewed on its own. (1) `is_slug` now validates its `separator` the way `slugify` has since SUTIL-101: a non-string raises the library's `InvalidInputError`, and an empty string raises `ValueError` with the message `separator must be a non-empty string`. Before this change `is_slug('hello-world', None)` failed inside `re` with a message that never mentioned the separator, and `is_slug('hello', '')` returned True while `slugify` rejects the same separator (the open decision recorded on SUTIL-104). (2) A behavior-preserving refactor of the `string_utils` package: the five star imports were replaced with explicit imports and `__init__.py` gained an `__all__` listing the same 42 public names; `validation.py` and `manipulation.py` now import `re` themselves instead of receiving it through a star import; `str.format` calls in the package became f-strings; `is_credit_card`'s `card_type` is annotated `Optional[str]`; `Generator` is imported from `collections.abc` and `list[str]` replaces `typing.List`; the `# -*- coding: utf-8 -*-` lines were removed. (3) Packaging: `pyproject.toml` (setuptools backend, `requires-python = ">=3.9"`, classifiers 3.9–3.14) replaces `setup.py`; `build.sh` and `MANIFEST` were deleted; `tox.ini` runs py39 through py314 with the same `python -m unittest` command.
- Files changed: `string_utils/__init__.py`, `string_utils/_regex.py`, `string_utils/errors.py`, `string_utils/generation.py`, `string_utils/manipulation.py`, `string_utils/validation.py`; `tests/test_is_slug.py` (two new tests, in the bug-fix commit only); `pyproject.toml` (new); `tox.ini`; `setup.py`, `build.sh`, `MANIFEST` (deleted).
- Commands run and observed results:
  - `python -m unittest` (baseline, before any change): Ran 410 tests — OK.
  - `python -m unittest tests.test_is_slug` (two new tests added, fix not yet applied): Ran 11 tests — FAILED (failures=2). The two new tests were seen failing.
  - `python -m unittest` (after the fix): Ran 412 tests — OK.
  - `python -m unittest` (after the refactor): Ran 412 tests — OK. `git status --short` showed changes under `string_utils/` only; no file under `tests/` changed.
  - Public API surface, `sorted(n for n in dir(string_utils) if not n.startswith('_'))`, saved before the refactor and compared after: identical, 46 names (42 functions plus the four module names).
  - `python -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"`: parses; project name `python-string-utils`, requires-python `>=3.9`.
  - `python -W error::DeprecationWarning -m unittest` (after the modernization): Ran 412 tests — OK.
  - Reproductions after the fix: `is_slug('hello-world', None)` ends with `InvalidInputError: Expected "str", received "NoneType"`; `is_slug('hello', '')` ends with `ValueError: separator must be a non-empty string`.
- Not claimed: no build or install was run from `pyproject.toml`; only Python 3.14 was executed here, so compatibility with 3.9 through 3.13 is declared, not tested; the refactor was checked by reading the diff and by the three checks above, not by a second reviewer.
- Unresolved questions:
  - `dev.requirements.txt` pins Sphinx, twine, tox and related tools to 2019–2020 versions. Left alone because nothing in this environment can verify an update.
  - `.travis.yml` describes a CI pipeline that no longer runs; `.readthedocs.yml` requests Python 3.5; the README badges list 3.5–3.8; `CHANGELOG.md` describes the Travis setup. All still say the old matrix.
  - The ticket asked for a Python 3.9 floor; 3.9 reached end-of-life in October 2025. Whether the floor should be 3.10 (which would also allow `str | None` in annotations) is a product decision for the owner.

## Unresolved questions

- `.travis.yml`, `.readthedocs.yml`, the README badges, and `CHANGELOG.md` still describe the old Python 3.5–3.8 matrix and the Travis pipeline, while `tox.ini` and `pyproject.toml` now say 3.9–3.14. Whether the floor should move to 3.10 is a product decision for the owner (see SUTIL-105).
- Release practice is still unconfirmed: `pyproject.toml` replaces `setup.py` and `build.sh`, but no build or install has been run from it, current release steps have not been verified with a maintainer, and `dev.requirements.txt` still pins 2019–2020 tool versions.
