# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Uses `uv` as the package manager.

```bash
uv sync                          # Install dependencies
uv run pytest                    # Run all tests
uv run pytest --cov              # Run tests with coverage (80% threshold required)
uv run pytest tests/test_foo.py  # Run a single test file
uv run second_brain              # Run the CLI
uv run --env-file .env second_brain  # Run with dev env vars
```

Linting and formatting use **Ruff** (line length 88, double quotes):
```bash
uv run ruff check .
uv run ruff format .
```

## Architecture

Three core modules:

- **`second_brain/cli.py`** — Click CLI group with three commands: `new <TITLE>`, `list`, `show <NUMBER>`. Commands delegate all business logic to `notes.py`.
- **`second_brain/notes.py`** — Pure business logic: `slugify()`, `build_note_path()`, `create_note()`. No I/O side effects except filesystem writes in `create_note`.
- **`second_brain/app.py`** — `configure_logging()` sets up Loguru with stderr + optional file handler. Called once at CLI startup.

Notes are stored as markdown files named `YYYY-MM-DD-<slug>.md` under `SECOND_BRAIN_DIR` (default `~/second_brain`). Duplicate filenames get a `-N` numeric suffix.

Environment variables: `SECOND_BRAIN_DIR`, `LOG_LEVEL`, `LOG_FILE` — see `.env.example` for dev defaults.
