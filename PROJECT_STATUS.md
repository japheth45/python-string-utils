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

## Unresolved questions

- `tox.ini` and `.travis.yml` list Python 3.5 through 3.8, but the environment runs a much newer Python and the suite passes. The project's supported-version policy is unconfirmed.
- Release and packaging practice is unconfirmed: `setup.py` and `build.sh` exist, but current release steps have not been verified with a maintainer.
