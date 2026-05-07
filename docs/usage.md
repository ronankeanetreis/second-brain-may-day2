# Usage

## Installation

Clone the repository and install dependencies:

```bash
uv sync
```

## Running

Via the CLI entrypoint:

```bash
uv run second_brain                          # production defaults
uv run --env-file .env second_brain          # dev settings
```

Or as a Python module:

```bash
uv run python -m second_brain
```

## Environment Variables

| Variable    | Default    | Description                          |
|-------------|------------|--------------------------------------|
| `LOG_LEVEL` | `INFO`     | Console log level (DEBUG, INFO, …)   |
| `LOG_FILE`  | `app.log`  | Path to the log file                 |

Copy `.env.example` to `.env` for development defaults, then run with `uv run --env-file .env`.

## Log Format

Console and file output use a compact format:

```
2026-04-11 21:21:47 | I | second_brain.app:main:29 | Hello from second_brain!
```

Log levels are shortened to a single letter:

| Full name | Short |
|-----------|-------|
| DEBUG     | D     |
| INFO      | I     |
| WARNING   | W     |
| ERROR     | E     |
| CRITICAL  | C     |
