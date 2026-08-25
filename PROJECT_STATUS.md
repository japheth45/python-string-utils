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

## Unresolved questions

- `tox.ini` and `.travis.yml` list Python 3.5 through 3.8, but the environment runs a much newer Python and the suite passes. The project's supported-version policy is unconfirmed.
- Release and packaging practice is unconfirmed: `setup.py` and `build.sh` exist, but current release steps have not been verified with a maintainer.
